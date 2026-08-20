"""
Deterministic security knowledge base.

Maps detection rule IDs to vulnerability intelligence: CWE, CVE (where a
specific instance is known -- usually "N/A" for behavioral detections),
MITRE ATT&CK techniques, and baseline impact/containment/remediation/
verification text.

This is the "evidence of record" layer described in the v15 architecture:

    Detection Engine -> Threat/Vulnerability Intelligence -> AI Security Analyst

The AI Security Analyst (sentinelcore.analysis.analyst) is NOT allowed to
invent or override CWE/CVE/MITRE values -- those are looked up here, not
generated. The AI may only add explanation, prioritization framing, and
remediation/verification wording, and even then the deterministic baseline
below is always the fallback if the AI is unavailable or returns something
unusable.
"""
from __future__ import annotations
from typing import Any

DEFAULT_ENTRY: dict[str, Any] = {
    "cwe": "N/A",
    "cve": "N/A",
    "vulnerability": "Unclassified security finding",
    "mitre_attack": [],
    "impact_baseline": "Potential security impact; review the event and affected asset.",
    "containment_baseline": "Review the event and, if warranted, isolate the affected asset or account.",
    "remediation_baseline": [
        "Investigate the event.",
        "Confirm scope of impact.",
        "Apply relevant hardening controls.",
    ],
    "verification_baseline": "Confirm the underlying condition no longer reproduces and monitor for recurrence.",
}

_KNOWLEDGE_BASE: dict[str, dict[str, Any]] = {
    "AUTH-001": {
        "cwe": "CWE-307",
        "cve": "N/A",
        "vulnerability": "Weak Authentication Controls",
        "mitre_attack": [{"id": "T1110", "name": "Brute Force"}],
        "impact_baseline": "Possible unauthorized access to a privileged account.",
        "containment_baseline": "Apply authentication rate limiting and temporarily lock the targeted account.",
        "remediation_baseline": [
            "Enable multi-factor authentication.",
            "Enforce authentication rate limiting / lockout thresholds.",
            "Review the account's recent session and access history.",
            "Reset credentials if compromise is confirmed.",
        ],
        "verification_baseline": "Monitor authentication telemetry for the account and confirm failures have stopped.",
    },
    "CRED-001": {
        "cwe": "CWE-307",
        "cve": "N/A",
        "vulnerability": "Weak Authentication Controls",
        "mitre_attack": [
            {"id": "T1110", "name": "Brute Force"},
            {"id": "T1110.004", "name": "Credential Stuffing"},
        ],
        "impact_baseline": "Possible unauthorized account access following a credential-stuffing pattern.",
        "containment_baseline": "Apply authentication rate limiting and investigate affected accounts.",
        "remediation_baseline": [
            "Enable MFA.",
            "Enforce rate limiting.",
            "Detect breached credentials.",
            "Review suspicious sessions.",
            "Reset compromised credentials where necessary.",
        ],
        "verification_baseline": "Monitor authentication telemetry and confirm the abnormal pattern has stopped.",
    },
    "MAL-001": {
        "cwe": "CWE-506",
        "cve": "N/A",
        "vulnerability": "Malicious Code Execution",
        "mitre_attack": [
            {"id": "T1204", "name": "User Execution"},
            {"id": "T1486", "name": "Data Encrypted for Impact"},
        ],
        "impact_baseline": "Potential malware or ransomware activity on the affected asset.",
        "containment_baseline": "Isolate the affected asset from the network immediately.",
        "remediation_baseline": [
            "Isolate and image the affected host for forensics.",
            "Run an endpoint detection and response scan across the fleet.",
            "Identify and block the malware's indicators of compromise.",
            "Restore from known-clean backups if encryption occurred.",
        ],
        "verification_baseline": "Confirm the host is clean via EDR re-scan and that no lateral spread occurred.",
    },
    "EXFIL-001": {
        "cwe": "CWE-200",
        "cve": "N/A",
        "vulnerability": "Exposure of Sensitive Information / Data Exfiltration",
        "mitre_attack": [{"id": "T1041", "name": "Exfiltration Over C2 Channel"}],
        "impact_baseline": "Possible unauthorized transfer of sensitive data outside the organization.",
        "containment_baseline": "Block the destination and suspend the initiating account or process pending review.",
        "remediation_baseline": [
            "Identify what data was transferred and its sensitivity.",
            "Block the destination IP/domain at the network egress.",
            "Review DLP policies and egress monitoring coverage.",
            "Notify data owners / compliance if sensitive data exposure is confirmed.",
        ],
        "verification_baseline": "Confirm no further transfers to the destination and that egress alerting is active.",
    },
    "PRIV-001": {
        "cwe": "CWE-269",
        "cve": "N/A",
        "vulnerability": "Improper Privilege Management",
        "mitre_attack": [
            {"id": "T1078", "name": "Valid Accounts"},
            {"id": "T1098", "name": "Account Manipulation"},
        ],
        "impact_baseline": "An account may have gained unauthorized elevated privileges.",
        "containment_baseline": "Revert the privilege change and disable the account pending investigation.",
        "remediation_baseline": [
            "Revert unauthorized group/role membership changes.",
            "Review who made the change and whether it was authorized.",
            "Audit other recent privilege changes by the same actor.",
            "Tighten the approval workflow for privileged group changes.",
        ],
        "verification_baseline": "Confirm the account's privilege level matches policy and the change is logged/approved.",
    },
}


def lookup(rule_id: str) -> dict[str, Any]:
    """Look up deterministic vulnerability intelligence for a rule ID.

    Always returns a complete entry (falling back to DEFAULT_ENTRY for any
    missing keys) so downstream code never has to special-case unknown
    rules. Returns a fresh dict each call so callers can't mutate the
    shared knowledge base.
    """
    entry = _KNOWLEDGE_BASE.get(rule_id, {})
    return {**DEFAULT_ENTRY, **entry}


def known_rule_ids() -> list[str]:
    return sorted(_KNOWLEDGE_BASE.keys())
