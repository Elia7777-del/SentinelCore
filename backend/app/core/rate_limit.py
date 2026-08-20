from collections import defaultdict, deque
from time import monotonic
from fastapi import HTTPException

_windows = defaultdict(deque)

def enforce_rate_limit(key: str, limit: int = 10, window_seconds: int = 60):
    now = monotonic()
    q = _windows[key]
    while q and now - q[0] > window_seconds:
        q.popleft()
    if len(q) >= limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    q.append(now)
