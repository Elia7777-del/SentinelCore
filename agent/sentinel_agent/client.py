import httpx
from .config import settings

def send_event(event: dict) -> dict:
    if not settings.agent_token:
        raise RuntimeError("SENTINEL_AGENT_TOKEN is not configured")
    url = settings.server_url.rstrip("/") + "/api/v1/events"
    headers = {"X-Sentinel-Agent-Token": settings.agent_token}
    with httpx.Client(verify=settings.verify_tls, timeout=15) as client:
        response = client.post(url, json=event, headers=headers)
        response.raise_for_status()
        return response.json()
