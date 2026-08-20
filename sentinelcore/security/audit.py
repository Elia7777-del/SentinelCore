"""Append-only audit helpers."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from typing import Any
from sentinelcore.core.models import AuditRecord

class AuditLog:
    def __init__(self, path: str = "data/audit.log"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, record: AuditRecord) -> str:
        payload = {
            "record_id": record.record_id,
            "timestamp": record.timestamp,
            "actor": record.actor,
            "action": record.action,
            "target": record.target,
            "outcome": record.outcome,
            "details": record.details,
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        payload["integrity_hash"] = hashlib.sha256(raw).hexdigest()
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, sort_keys=True) + "\n")
        return payload["integrity_hash"]
