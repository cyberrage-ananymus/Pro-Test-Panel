import asyncio
import secrets
import socket
from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect

from main import (
    LINKS,
    LINKS_LOCK,
    stats,
    hourly_traffic,
    connections,
    error_logs,
    logger,
    is_link_allowed,
    is_ip_allowed,
    save_state,
    log_activity,
    now_ir,
)
from speed_limit import throttle

RELAY_BUF = 4 * 1024 * 1024
BATCH_THRESHOLD = 100


def _ws_client_ip(ws: WebSocket) -> str:
    fwd = ws.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    real_ip = ws.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return ws.client.host if ws.client else "unknown"


def _tune_socket(writer: asyncio.StreamWriter):
    sock = writer.transport.get_extra_info("socket")
    if not sock:
        return
    try:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 16 * 1024 * 1024)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 16 * 1024 * 1024)
    except OSError:
        pass
    try:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 0)
    except (OSError, AttributeError):
        pass


async def parse_vless_header(chunk: bytes):
    if len(chunk) < 24:
        raise ValueError("chunk too small")
    pos = 1
    pos += 16
    addon_len = chunk[pos]; pos += 1 + addon_len
    command = chunk[pos]; pos += 1
    port = int.from_bytes(chunk[pos:pos+2], "big"); pos += 2
    addr_type = chunk[pos]; pos += 1
    if addr_type == 1:
        address = ".".join(str(b) for b in chunk[pos:pos+4]); pos += 4
    elif addr_type == 2:
        dlen = chunk[pos]; pos += 1
        address = chunk[pos:pos+dlen].decode("utf-8", errors="ignore"); pos += dlen
    elif addr_type == 3:
        ab = chunk[pos:pos+16]; pos += 16
        address = ":".join(f"{ab[i]:02x}{ab[i+1]:02x}" for i in range(0, 16, 2))
    else:
        raise ValueError(f"unknown addr type: {addr_type}")
    return command, address, port, chunk[pos:]


async def check_and_use(uid: str, n: int) -> bool:
    async with LINKS_LOCK:
        link = LINKS.get(uid)
        if link is None:
            return False
        if not is_link_allowed(link):
            return False
        link["used_bytes"] += n
        stats["total_bytes"] += n
    return True


async def relay_ws_to_tcp(ws: WebSocket, writer: asyncio.StreamWriter, conn_id: str, uid: str):
    pending_bytes = 0
    pending_reqs = 0
    try:
        while True:
            msg = await ws.receive()
            if msg["type"] == "websocket.disconnect":
                break
            data = msg.get("bytes") or (msg.get("text") or "").encode()
            if not data:
                continue
            nd = len(data)
            pending_bytes += nd
            pending_reqs += 1
            if pending_reqs >= BATCH_THRESHOLD:
                hourly_traffic[now_ir().strftime("%H:00")] += pending_bytes
                if not await check_and_use(uid, pending_bytes):
                    await ws.close(code=1008, reason="quota/disabled/unknown")
                    break
                await throttle(uid, pending_bytes)
                stats["total_requests"] += pending_reqs
                connections[conn_id]["bytes"] += pending_bytes
                pending_bytes = 0
                pending_reqs = 0
            writer.write(data)
            if writer.transport.get_write_buffer_size() > RELAY_BUF:
                await writer.drain()
        if pending_bytes > 0:
            hourly_traffic[now_ir().strftime("%H:00")] += pending_bytes
            if await check_and_use(uid, pending_bytes):
                await throttle(uid, pending_bytes)
                stats["total_requests"] += pending_reqs
                connections[conn_id]["bytes"] += pending_bytes
    except (WebSocketDisconnect, Exception):
        pass
    finally:
        try:
            writer.write_eof()
        except Exception:
            pass


async def relay_tcp_to_ws(ws: WebSocket, reader: asyncio.StreamReader, conn_id: str, uid: str):
    first = True
    pending_bytes = 0
    pending_reqs = 0
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break
            nd = len(data)
            pending_bytes += nd
            pending_reqs += 1
            if pending_reqs >= BATCH_THRESHOLD:
                hourly_traffic[now_ir().strftime("%H:00")] += pending_bytes
                if not await check_and_use(uid, pending_bytes):
                    await ws.close(code=1008, reason="quota/disabled/unknown")
                    break
                await throttle(uid, pending_bytes)
                connections[conn_id]["bytes"] += pending_bytes
                pending_bytes = 0
                pending_reqs = 0
            payload = (b"\x00\x00" + data) if first else data
            first = False
            await ws.send_bytes(payload)
        if pending_bytes > 0:
            hourly_traffic[now_ir().strftime("%H:00")] += pending_bytes
            if await check_and_use(uid, pending_bytes):
                await throttle(uid, pending_bytes)
                connections[conn_id]["bytes"] += pending_bytes
    except Exception:
        pass


async def websocket_tunnel(ws: WebSocket, uuid: str):
    await ws.accept()

    async with LINKS_LOCK:
        link = LINKS.get(uuid)

    if not is_link_allowed(link):
        await ws.close(code=1008, reason="not authorized")
        return

    ip = _ws_client_ip(ws)

    if not is_ip_allowed(link, uuid, ip):
        log_activity("connection", f"Rejected {ip} (IP limit)", "warn")
        await ws.close(code=1008, reason="ip limit reached")
        return

    conn_id = secrets.token_urlsafe(6)
    connections[conn_id] = {
        "uuid": uuid,
        "ip": ip,
        "transport": "vless-ws",
        "connected_at": datetime.now().isoformat(),
        "bytes": 0,
    }
    writer = None

    try:
        first_msg = await asyncio.wait_for(ws.receive(), timeout=15.0)
        if first_msg["type"] == "websocket.disconnect":
            return
        first_chunk = first_msg.get("bytes") or (first_msg.get("text") or "").encode()
        if not first_chunk:
            return

        command, address, port, payload = await parse_vless_header(first_chunk)

        if not await check_and_use(uuid, len(first_chunk)):
            await ws.close(code=1008, reason="quota/disabled")
            return

        hourly_traffic[now_ir().strftime("%H:00")] += len(first_chunk)
        stats["total_requests"] += 1
        connections[conn_id]["bytes"] += len(first_chunk)

        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(address, port),
            timeout=10.0
        )
        _tune_socket(writer)

        if payload:
            writer.write(payload)
            await writer.drain()

        done, pending = await asyncio.wait(
            {
                asyncio.create_task(relay_ws_to_tcp(ws, writer, conn_id, uuid)),
                asyncio.create_task(relay_tcp_to_ws(ws, reader, conn_id, uuid)),
            },
            return_when=asyncio.FIRST_COMPLETED,
        )
        for t in pending:
            t.cancel()
            try:
                await t
            except asyncio.CancelledError:
                pass

        asyncio.create_task(save_state())

    except WebSocketDisconnect:
        pass
    except asyncio.TimeoutError:
        stats["total_errors"] += 1
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "time": datetime.now().isoformat()})
    finally:
        if writer:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        connections.pop(conn_id, None)
