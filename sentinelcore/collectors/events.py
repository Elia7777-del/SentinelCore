"""Event normalization and collection contracts."""
from __future__ import annotations
from typing import Any
from sentinelcore.core.models import SecurityEvent, utc_now

def normalize_event(raw: dict[str, Any], source: str = "unknown") -> SecurityEvent:
    return SecurityEvent(
        event_id=str(raw.get("event_id") or raw.get("id") or f"evt-{hash(str(raw)) & 0xffffffff:x}"),
        timestamp=str(raw.get("timestamp") or utc_now()),
        source=source,
        event_type=str(raw.get("event_type") or raw.get("type") or "unknown"),
        severity=str(raw.get("severity") or "Info"),
        asset_id=raw.get("asset_id"),
        user_id=raw.get("user_id"),
        source_ip=raw.get("source_ip"),
        destination_ip=raw.get("destination_ip"),
        message=str(raw.get("message") or ""),
        metadata=dict(raw.get("metadata") or {}),
    )
