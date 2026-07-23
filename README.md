# Cyber-Rage-Panel-Speed

High-throughput VLESS gateway with WebSocket and adaptive XHTTP transport, plus a live admin dashboard.

## Features

- **VLESS gateway** over WebSocket (`vless-ws`) and XHTTP (`xhttp-packet-up`, `xhttp-stream-up`) transports
- **Adaptive XHTTP engine** — flow-control window and upload batching self-tune to real-time drain speed instead of using fixed sizes
- **Config management** — create, edit, disable, and delete VLESS configs with per-config traffic caps, expiry, speed limits, and IP limits
- **Day-elapsed tracking** — each config shows a live progress bar for how many of its allotted days have passed, plus "Xd left" / "expired Xd ago"
- **Live connections monitor** — active connections grouped by IP, with sessions, transport, and data used
- **IP geolocation** — every connected IP is resolved to a city/country (ISP on hover) and cached in memory, so a config being used from unexpected countries stands out immediately
- **Sub-groups** — bundle multiple configs into one subscription URL or public usage page
- **Dashboard** — live traffic charts (24h overview + full hourly breakdown), recent activity log, and a proxy-error log
- **Password-protected admin panel** with a signed session cookie

## Speed Optimizations

| Component | Setting | Value |
|---|---|---|
| WS relay read buffer | `RELAY_BUF` | 4 MB |
| XHTTP downlink read buffer | `XHTTP_BUF` | 4 MB |
| Socket send/recv buffers | `SO_SNDBUF` / `SO_RCVBUF` | 16 MB |
| XHTTP downlink queue depth | `DOWNLINK_QUEUE_MAX` | 2048 chunks |
| XHTTP stream-up flow window | `FLOW_MIN_HW` – `FLOW_MAX_HW` | 1 MB – 128 MB (adaptive) |
| XHTTP packet-up quota batch | `QUOTA_MIN_BATCH` – `QUOTA_MAX_BATCH` | 128 KB – 8 MB (adaptive, EWMA-timed) |
| Idle session cleanup | `SESSION_IDLE_TIMEOUT` / `REAPER_INTERVAL` | 30s / 10s |
| Upstream TCP connect timeout | `TCP_CONNECT_TIMEOUT` | 10s |

## Deploy on Railway

1. Fork this repository
2. Go to [Railway.app](https://railway.app/) → New Project → Deploy from GitHub repo
3. Select your forked repo
4. Go to Settings → Networking → Generate Domain
5. Add a Volume mounted at `/data` for persistent storage

## Deploy on VPS

```bash
git clone <your-repo>
cd Cyber-Rage-Panel-Speed
pip install -r requirements.txt
python main.py
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `PORT` | Port the server listens on | `8000` |
| `ADMIN_PASSWORD` | Dashboard login password | `CYBERRAGE` |
| `SECRET_KEY` | Session-signing secret (auto-generated & persisted to disk if unset) | random |
| `DATA_DIR` | Directory for persisted state (configs, groups, secret) | `/data` |
| `RAILWAY_PUBLIC_DOMAIN` | Public hostname used to build VLESS/subscription links | `localhost` |

## Default Credentials

- Password: `CYBERRAGE`

**Change this immediately after first deploy** by setting `ADMIN_PASSWORD` (there's no in-dashboard password-change screen yet, only the `/api/change-password` endpoint).

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/login` / `/api/logout` | POST | Start / end an admin session |
| `/api/me` | GET | Current session info |
| `/api/change-password` | POST | Change the admin password |
| `/api/links` | GET / POST | List / create VLESS configs |
| `/api/links/{uid}` | PATCH / DELETE | Update / remove a config |
| `/api/subs` | GET / POST | List / create sub-groups |
| `/api/subs/{sub_id}` | PATCH / DELETE | Update / remove a sub-group |
| `/api/subs/{sub_id}/links` | POST | Attach configs to a sub-group |
| `/api/connections` | GET | Active connections grouped by IP, with geolocation |
| `/api/activity` | GET | Recent activity log |
| `/stats` | GET | Dashboard metrics, hourly traffic history, proxy error log |
| `/sub/{uuid}` | GET | Subscription file for a single config |
| `/sub-group/{uuid_key}` | GET | Subscription file for a group |
| `/p/{uuid_key}` | GET | Public usage page for a group |
| `/ws/{uuid}` | WS | VLESS-over-WebSocket tunnel |
| `/xhttp-siz10/{mode}/{uuid}/{session_id}` | GET | XHTTP downlink stream |
| `/xhttp-siz10/packet-up/{uuid}/{session_id}/{seq}` | POST | XHTTP packet-mode uplink |
| `/xhttp-siz10/stream-up/{uuid}/{session_id}` | POST | XHTTP stream-mode uplink |

## Tech Stack

- **Backend:** Python 3.11+ / FastAPI / Uvicorn / httpx
- **Frontend:** Space Grotesk / JetBrains Mono / Phosphor Icons / Chart.js
- **Transport:** VLESS over WebSocket & XHTTP (packet-up and stream-up modes)
- **Geolocation:** ip-api.com free tier, in-memory cached
- **Storage:** JSON file on disk
