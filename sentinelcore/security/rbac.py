"""RBAC primitives for SentinelCore administration."""
from __future__ import annotations
from dataclasses import dataclass

ROLES = {
    "system_admin",
    "security_admin",
    "soc_analyst",
    "incident_responder",
    "threat_hunter",
    "auditor",
    "executive",
    "read_only",
}

@dataclass(frozen=True)
class Principal:
    user_id: str
    role: str
    mfa_verified: bool = False

def authorize(principal: Principal, allowed_roles: set[str]) -> bool:
    if principal.role not in ROLES:
        return False
    return principal.role in allowed_roles

def require_mfa(principal: Principal) -> None:
    if not principal.mfa_verified:
        raise PermissionError("MFA verification is required for this action.")
