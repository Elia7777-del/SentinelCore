from app.services.audit_chain import build_audit_record

def test_audit_chain_links_events():
    first = build_audit_record("login", "u1", "org1", {}, "0" * 64)
    second = build_audit_record("view_incident", "u1", "org1", {}, first["event_hash"])
    assert second["previous_hash"] == first["event_hash"]
    assert second["event_hash"] != first["event_hash"]
