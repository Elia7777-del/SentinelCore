from datetime import datetime, timedelta, timezone
import hashlib
import secrets

def issue_token(ttl_hours: int = 24) -> tuple[str, str, datetime]:
    raw = secrets.token_urlsafe(32)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    expires = datetime.now(timezone.utc) + timedelta(hours=ttl_hours)
    return raw, digest, expires

def hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
