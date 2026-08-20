"""Contextual risk scoring."""
from __future__ import annotations

SEVERITY = {"Critical": 100, "High": 75, "Medium": 50, "Low": 25, "Info": 0}
CRITICALITY = {"Critical": 1.0, "High": .85, "Medium": .65, "Low": .4}

def calculate_risk(threat_severity: str, asset_criticality: str = "Medium",
                   exposure: float = 1.0, confidence: float = 1.0) -> int:
    base = SEVERITY.get(threat_severity.title(), 0)
    context = CRITICALITY.get(asset_criticality.title(), .65)
    score = base * context * max(0.0, min(1.0, exposure)) * max(0.0, min(1.0, confidence))
    return max(0, min(100, round(score)))

def risk_level(score: int) -> str:
    if score >= 80: return "Critical"
    if score >= 60: return "High"
    if score >= 30: return "Medium"
    if score > 0: return "Low"
    return "Info"
