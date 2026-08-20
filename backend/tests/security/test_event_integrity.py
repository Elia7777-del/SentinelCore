from app.services.event_integrity import event_digest

def test_digest_is_stable():
    a = {"b": 2, "a": 1}
    b = {"a": 1, "b": 2}
    assert event_digest(a) == event_digest(b)

def test_digest_changes_when_event_changes():
    assert event_digest({"a": 1}) != event_digest({"a": 2})
