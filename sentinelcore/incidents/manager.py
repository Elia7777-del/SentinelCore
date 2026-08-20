"""Incident lifecycle management."""
from __future__ import annotations
import uuid
from sentinelcore.core.models import Incident, utc_now

VALID_STATES = ["Detected", "Triaged", "Investigating", "Contained", "Remediating", "Resolved", "Closed"]

class IncidentManager:
    def create(self, title: str, severity: str, risk_score: int = 0,
               assets: list[str] | None = None) -> Incident:
        now = utc_now()
        return Incident(
            incident_id=f"INC-{uuid.uuid4().hex[:10].upper()}",
            title=title, severity=severity, risk_score=risk_score,
            created_at=now, updated_at=now,
            affected_assets=assets or [],
        )

    def transition(self, incident: Incident, new_status: str) -> Incident:
        if new_status not in VALID_STATES:
            raise ValueError(f"Unsupported incident status: {new_status}")
        incident.status = new_status
        incident.updated_at = utc_now()
        return incident
