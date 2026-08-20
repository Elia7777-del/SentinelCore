"""Rule-based defensive detection engine.

Deterministic detections are the evidence layer for SentinelCore's AI
Security Analyst: every Detection here is backed by an explicit,
inspectable condition -- never an AI guess. Rule IDs map to CWE/CVE/
MITRE ATT&CK data in sentinelcore.intelligence.knowledge_base.

Per-organization tuning (which rules are enabled, and threshold values)
is supported via DetectionConfig, so a multi-tenant deployment doesn't
have to ship one fixed rule set for every customer.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from sentinelcore.core.models import SecurityEvent

ALL_RULE_IDS = ("CRED-001", "AUTH-001", "MAL-001", "EXFIL-001", "PRIV-001")


@dataclass
class Detection:
    rule_id: str
    title: str
    severity: str
    confidence: str
    reason: str
    event_id: str


@dataclass
class DetectionConfig:
    """Per-organization tuning for the detection engine.

    disabled_rules: rule IDs to skip entirely for this org (e.g. an org
        with no file-transfer visibility might disable EXFIL-001 rather
        than get noisy false negatives).
    cred_stuffing_failed_attempts: failed-login count that, together with
        a subsequent success, triggers CRED-001. Lower for a smaller org
        with tight login SLAs, raise for a high-traffic consumer app
        where a handful of failures is normal.
    exfil_bytes_out_threshold: bytes transferred that flags EXFIL-001 on
        its own, independent of message content.
    """

    disabled_rules: frozenset[str] = field(default_factory=frozenset)
    cred_stuffing_failed_attempts: int = 5
    exfil_bytes_out_threshold: int = 500_000_000

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "DetectionConfig":
        data = data or {}
        disabled = data.get("disabled_rules") or []
        thresholds = data.get("thresholds") or {}
        return cls(
            disabled_rules=frozenset(r for r in disabled if r in ALL_RULE_IDS),
            cred_stuffing_failed_attempts=int(
                thresholds.get("cred_stuffing_failed_attempts", 5)
            ),
            exfil_bytes_out_threshold=int(
                thresholds.get("exfil_bytes_out_threshold", 500_000_000)
            ),
        )


class DetectionEngine:
    """Evaluates a SecurityEvent against all registered detection rules.

    Rules are intentionally simple and explicit. Each one inspects the
    event message and/or structured metadata and returns zero or more
    Detections -- there is no scoring ambiguity or AI involvement at this
    layer, so every Detection can be traced back to a concrete condition.
    """

    def __init__(self, config: DetectionConfig | None = None) -> None:
        self.config = config or DetectionConfig()

    def detect(self, event: SecurityEvent) -> list[Detection]:
        msg = (event.message or "").lower()
        meta = event.metadata or {}
        disabled = self.config.disabled_rules

        detections: list[Detection] = []
        if "CRED-001" not in disabled:
            detections += self._check_credential_stuffing(event, msg, meta)
        if "AUTH-001" not in disabled:
            detections += self._check_privileged_auth_failure(event, msg)
        if "MAL-001" not in disabled:
            detections += self._check_malware(event, msg)
        if "EXFIL-001" not in disabled:
            detections += self._check_exfiltration(event, msg, meta)
        if "PRIV-001" not in disabled:
            detections += self._check_privilege_escalation(event, msg)
        return detections

    def _check_credential_stuffing(
        self, event: SecurityEvent, msg: str, meta: dict[str, Any]
    ) -> list[Detection]:
        failed_attempts = meta.get("failed_attempts")
        outcome = str(meta.get("outcome", "")).lower()

        metadata_match = (
            isinstance(failed_attempts, (int, float))
            and failed_attempts >= self.config.cred_stuffing_failed_attempts
            and outcome == "success"
        )
        message_match = "credential stuffing" in msg or (
            "failed login" in msg and "successful login" in msg
        )

        if not (metadata_match or message_match):
            return []

        note = ""
        if isinstance(failed_attempts, (int, float)):
            note = f" ({int(failed_attempts)} failed attempts before success)"

        return [
            Detection(
                "CRED-001",
                "Credential Stuffing",
                "High",
                "High",
                f"Multiple authentication failures followed by a successful login attempt{note}.",
                event.event_id,
            )
        ]

    def _check_privileged_auth_failure(
        self, event: SecurityEvent, msg: str
    ) -> list[Detection]:
        if "failed login" in msg and "admin" in msg:
            return [
                Detection(
                    "AUTH-001",
                    "Suspicious privileged authentication activity",
                    "High",
                    "Medium",
                    "A privileged authentication failure pattern was observed.",
                    event.event_id,
                )
            ]
        return []

    def _check_malware(self, event: SecurityEvent, msg: str) -> list[Detection]:
        if "malware" in msg or "ransomware" in msg:
            return [
                Detection(
                    "MAL-001",
                    "Potential malware activity",
                    "Critical",
                    "High",
                    "The event contains a known malware-related indicator.",
                    event.event_id,
                )
            ]
        return []

    def _check_exfiltration(
        self, event: SecurityEvent, msg: str, meta: dict[str, Any]
    ) -> list[Detection]:
        bytes_out = meta.get("bytes_out")
        large_transfer = (
            isinstance(bytes_out, (int, float))
            and bytes_out >= self.config.exfil_bytes_out_threshold
        )

        if not ("exfiltration" in msg or "large outbound transfer" in msg or large_transfer):
            return []

        note = f" ({int(bytes_out):,} bytes transferred)" if large_transfer else ""
        return [
            Detection(
                "EXFIL-001",
                "Potential data exfiltration",
                "Critical",
                "Medium",
                f"An abnormally large or flagged outbound data transfer was observed{note}.",
                event.event_id,
            )
        ]

    def _check_privilege_escalation(
        self, event: SecurityEvent, msg: str
    ) -> list[Detection]:
        if (
            "privilege escalation" in msg
            or "added to admin group" in msg
            or "added to administrators" in msg
        ):
            return [
                Detection(
                    "PRIV-001",
                    "Potential privilege escalation",
                    "High",
                    "Medium",
                    "An account was observed gaining elevated privileges outside an expected workflow.",
                    event.event_id,
                )
            ]
        return []
