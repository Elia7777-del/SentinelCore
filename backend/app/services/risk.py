
SEVERITY = {"informational":1, "low":2, "medium":4, "high":7, "critical":10}
CRITICALITY = {"low":1, "medium":2, "high":4, "critical":5}

def calculate_risk(severity: str, asset_criticality: str, confidence: float = 1.0, exposure: float = 1.0) -> float:
    """Transparent, bounded risk score for triage; not a substitute for organizational risk policy."""
    s = SEVERITY.get(severity.lower(), 1)
    a = CRITICALITY.get(asset_criticality.lower(), 1)
    c = max(0.0, min(confidence, 1.0))
    e = max(0.0, min(exposure, 1.0))
    return round(min(100.0, s * a * c * e * 2.0), 2)
