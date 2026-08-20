from sentinelcore.core.risk import calculate_risk, risk_level
from sentinelcore.detection.engine import DetectionEngine
from sentinelcore.collectors.events import normalize_event

def test_risk_scoring():
    score = calculate_risk("High", "High", 1.0, 1.0)
    assert 0 <= score <= 100
    assert risk_level(score) in {"Critical", "High", "Medium", "Low", "Info"}

def test_event_normalization_and_detection():
    event = normalize_event({
        "id": "1",
        "type": "authentication",
        "message": "failed login for admin",
    }, source="test")
    detections = DetectionEngine().detect(event)
    assert detections
    assert detections[0].severity == "High"
