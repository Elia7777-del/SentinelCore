import hashlib
import json

def event_digest(event: dict) -> str:
    raw = json.dumps(event, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()
