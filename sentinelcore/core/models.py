"""Core domain models for SentinelCore."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class SecurityEvent:
    event_id: str
    timestamp: str
    source: str
    event_type: str
    severity: str = "Info"
    asset_id: str | None = None
    user_id: str | None = None
    source_ip: str | None = None
    destination_ip: str | None = None
    message: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Asset:
    asset_id: str
    hostname: str
    asset_type: str = "Unknown"
    criticality: str = "Medium"
    owner: str | None = None
    ip_address: str | None = None
    status: str = "Active"
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Incident:
    incident_id: str
    title: str
    severity: str
    status: str = "Detected"
    risk_score: int = 0
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    affected_assets: list[str] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

@dataclass
class AuditRecord:
    record_id: str
    timestamp: str
    actor: str
    action: str
    target: str
    outcome: str
    details: dict[str, Any] = field(default_factory=dict)
