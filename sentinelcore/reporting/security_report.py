"""Security report generation."""
from __future__ import annotations
import json
from datetime import datetime, timezone

def generate_report(summary: dict, incidents: list[dict] | None = None) -> str:
    report = {
        "product": "SentinelCore",
        "version": "4.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "incidents": incidents or [],
    }
    return json.dumps(report, indent=2)
