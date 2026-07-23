"""
Lightweight IP -> geolocation lookups for the Connections dashboard.

Uses ip-api.com's free batch endpoint (no API key, 45 req/min, HTTP only on
the free tier). Results are cached in-memory so a config's IP is only ever
looked up once every GEO_TTL seconds, no matter how often the dashboard
polls /api/connections.

Private/loopback/link-local addresses are never sent to the API; they're
labeled "Local" immediately.
"""

import ipaddress
import time

import httpx

GEO_TTL = 6 * 60 * 60  # re-check an IP after this many seconds
_MAX_BATCH = 100  # ip-api.com batch endpoint limit per request
_BATCH_URL = (
    "http://ip-api.com/batch"
    "?fields=status,message,query,country,countryCode,regionName,city,isp"
)

_GEO_CACHE: dict[str, dict] = {}


def _is_public_ip(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return not (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_reserved
        or addr.is_multicast
        or addr.is_unspecified
    )


def _entry(country=None, country_code=None, city=None, region=None, isp=None, label="Unknown") -> dict:
    return {
        "country": country,
        "country_code": country_code,
        "city": city,
        "region": region,
        "isp": isp,
        "label": label,
        "cached_at": time.time(),
    }


async def geolocate_ips(client: httpx.AsyncClient, ips: list[str]) -> dict[str, dict]:
    """Resolve IPs to geo info via cache + ip-api.com batch lookups.

    Returns {ip: {country, country_code, city, region, isp, label}}.
    Never raises; on any failure the affected IPs get an "Unknown" entry
    so the dashboard still renders.
    """
    now = time.time()
    to_fetch: list[str] = []

    for ip in dict.fromkeys(i for i in ips if i and i != "unknown"):
        cached = _GEO_CACHE.get(ip)
        if cached and (now - cached["cached_at"]) < GEO_TTL:
            continue
        if not _is_public_ip(ip):
            _GEO_CACHE[ip] = _entry(label="Local")
            continue
        to_fetch.append(ip)

    for i in range(0, len(to_fetch), _MAX_BATCH):
        chunk = to_fetch[i : i + _MAX_BATCH]
        try:
            resp = await client.post(_BATCH_URL, json=chunk, timeout=6.0)
            data = resp.json()
            for item in data:
                q = item.get("query")
                if not q:
                    continue
                if item.get("status") == "success":
                    city = item.get("city") or ""
                    cc = item.get("countryCode") or ""
                    label = ", ".join(p for p in [city, cc] if p) or item.get("country") or "Unknown"
                    _GEO_CACHE[q] = _entry(
                        country=item.get("country"),
                        country_code=cc or None,
                        city=item.get("city"),
                        region=item.get("regionName"),
                        isp=item.get("isp"),
                        label=label,
                    )
                else:
                    _GEO_CACHE[q] = _entry(label="Unknown")
        except Exception:
            for ip in chunk:
                if ip not in _GEO_CACHE:
                    _GEO_CACHE[ip] = _entry(label="Unknown")

    return {ip: _GEO_CACHE.get(ip, _entry(label="Unknown")) for ip in ips if ip and ip != "unknown"}
