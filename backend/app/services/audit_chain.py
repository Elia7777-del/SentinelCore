import hashlib
import json
from datetime import datetime, timezone

def canonical_event(event: dict) -> bytes:
    return json.dumps(event, sort_keys=True, separators=(",", ":")).encode()

def chain_hash(previous_hash: str, event: dict) -> str:
    material = previous_hash.encode() + canonical_event(event)
    return hashlib.sha256(material).hexdigest()

def build_audit_record(
    action: str,
    actor_id: str | None,
    organization_id: str,
    details: dict,
    previous_hash: str,
) -> dict:
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "actor_id": actor_id,
        "organization_id": organization_id,
        "details": details,
    }
    event["previous_hash"] = previous_hash
    event["event_hash"] = chain_hash(previous_hash, event)
    return event
