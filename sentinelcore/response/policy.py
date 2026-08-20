"""Policy-controlled response decisions."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ResponseDecision:
    action: str
    mode: str
    requires_approval: bool
    reason: str

def decide(severity: str, action: str, mode: str = "recommend") -> ResponseDecision:
    allowed_modes = {"alert", "recommend", "automatic", "approval"}
    if mode not in allowed_modes:
        raise ValueError("Invalid response mode.")
    requires = mode == "approval" or (mode == "automatic" and severity.title() == "Critical")
    return ResponseDecision(action, mode, requires, f"Policy decision for {severity} severity.")
