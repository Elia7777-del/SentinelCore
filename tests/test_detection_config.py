from sentinelcore.detection.engine import ALL_RULE_IDS, DetectionConfig, DetectionEngine
from sentinelcore.collectors.events import normalize_event


def _cred_stuffing_event(failed_attempts=9):
    return normalize_event(
        {
            "id": "evt-1",
            "type": "authentication",
            "message": "authentication attempts observed",
            "metadata": {"failed_attempts": failed_attempts, "outcome": "success"},
        },
        source="test",
    )


def test_default_config_matches_previous_hardcoded_threshold():
    engine = DetectionEngine()
    detections = engine.detect(_cred_stuffing_event(failed_attempts=5))
    assert any(d.rule_id == "CRED-001" for d in detections)


def test_disabled_rule_is_skipped():
    config = DetectionConfig(disabled_rules=frozenset({"CRED-001"}))
    engine = DetectionEngine(config=config)
    detections = engine.detect(_cred_stuffing_event(failed_attempts=20))
    assert not any(d.rule_id == "CRED-001" for d in detections)


def test_custom_threshold_is_respected():
    # Org wants a stricter policy: flag after 2 failures instead of 5.
    config = DetectionConfig(cred_stuffing_failed_attempts=2)
    engine = DetectionEngine(config=config)
    detections = engine.detect(_cred_stuffing_event(failed_attempts=3))
    assert any(d.rule_id == "CRED-001" for d in detections)

    # And 1 failure still shouldn't trigger it.
    detections = engine.detect(_cred_stuffing_event(failed_attempts=1))
    assert not any(d.rule_id == "CRED-001" for d in detections)


def test_from_dict_ignores_unknown_rule_ids():
    config = DetectionConfig.from_dict({"disabled_rules": ["CRED-001", "NOT-A-REAL-RULE"]})
    assert config.disabled_rules == frozenset({"CRED-001"})


def test_from_dict_defaults_when_empty():
    config = DetectionConfig.from_dict(None)
    assert config.disabled_rules == frozenset()
    assert config.cred_stuffing_failed_attempts == 5
    assert config.exfil_bytes_out_threshold == 500_000_000


def test_all_rule_ids_have_knowledge_base_entries():
    from sentinelcore.intelligence.knowledge_base import known_rule_ids

    assert set(ALL_RULE_IDS) == set(known_rule_ids())
