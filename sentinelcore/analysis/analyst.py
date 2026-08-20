"""
AI Security Analyst
--------------------

Implements the v15 pipeline stage:

    Security Event -> Detection Engine -> Threat/Vulnerability Intelligence
    -> AI Security Analyst -> Risk Score -> Incident

Design principle: the AI explains, prioritizes, and drafts remediation --
it never invents evidence. Facts (which rule fired, why, CVE, CWE, MITRE
ATT&CK technique, and the resulting severity/confidence floor) come
exclusively from the deterministic Detection Engine and knowledge base.

If no AI callable is configured, or the AI call fails / returns something
unusable, `analyze()` still returns a complete, correct analysis built
entirely from deterministic data. AI assistance is additive narrative
polish on top of a system that already works without it -- this keeps
SentinelCore safe from an AI "guessing" a vulnerability into existence.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from sentinelcore.core.models import SecurityEvent
from sentinelcore.core.risk import calculate_risk, risk_level
from sentinelcore.detection.engine import Detection, DetectionEngine
from sentinelcore.intelligence.knowledge_base import DEFAULT_ENTRY, lookup

SEVERITY_RANK = {"Info": 0, "Low": 1, "Medium": 2, "High": 3, "Critical": 4}
CONFIDENCE_FLOOR_BY_LEVEL = {"Low": 40, "Medium": 70, "High": 90}

# An AI callable takes the deterministic context dict and returns either a
# dict of narrative fields, or None if it has nothing useful to add. It
# must not raise for "no answer" -- callers still catch exceptions
# defensively, but returning None is the expected no-op path.
AnalystFn = Callable[[dict[str, Any]], Optional[dict[str, Any]]]


@dataclass
class SecurityAnalysis:
    schema_version: str
    event_id: str
    threat: str
    vulnerability: str
    cve: str
    cwe: str
    severity: str
    confidence: int
    evidence: list[str]
    impact: str
    immediate_containment: str
    recommended_remediation: list[str]
    mitre_attack: list[dict[str, str]]
    verification: str
    risk_score: int
    risk_level: str
    ai_assisted: bool
    source_rules: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "event_id": self.event_id,
            "threat": self.threat,
            "vulnerability": self.vulnerability,
            "cve": self.cve,
            "cwe": self.cwe,
            "severity": self.severity,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "impact": self.impact,
            "immediate_containment": self.immediate_containment,
            "recommended_remediation": self.recommended_remediation,
            "mitre_attack": self.mitre_attack,
            "verification": self.verification,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "ai_assisted": self.ai_assisted,
            "source_rules": self.source_rules,
        }


class AISecurityAnalyst:
    """Turns detections into a structured, decision-ready finding.

    `ai_fn`, if provided, is called with a plain-dict deterministic
    context and may return a dict of narrative fields (threat,
    vulnerability, impact, immediate_containment,
    recommended_remediation, verification). Any field it omits, or that
    isn't the right type, falls back to the deterministic knowledge-base
    baseline -- the analysis is never incomplete just because the AI
    layer had nothing to say.
    """

    SCHEMA_VERSION = "1.0"

    def __init__(
        self,
        detection_engine: DetectionEngine | None = None,
        ai_fn: AnalystFn | None = None,
    ) -> None:
        self.detection_engine = detection_engine or DetectionEngine()
        self.ai_fn = ai_fn

    def analyze(
        self,
        event: SecurityEvent,
        asset_criticality: str = "Medium",
        exposure: float = 1.0,
    ) -> SecurityAnalysis | None:
        """Run the full pipeline for one event. Returns None if no
        detection rule fired -- callers should treat that as "nothing to
        report", not as an error."""
        detections = self.detection_engine.detect(event)
        if not detections:
            return None

        kb_entries = [lookup(d.rule_id) for d in detections]

        evidence = [d.reason for d in detections]
        cwe = self._first_non_default(kb_entries, "cwe")
        cve = self._first_non_default(kb_entries, "cve")
        mitre = self._merge_mitre(kb_entries)

        severity_floor = self._severity_floor(detections)
        confidence_floor = self._confidence_floor(detections)

        risk_score = calculate_risk(
            severity_floor, asset_criticality, exposure, confidence_floor / 100.0
        )

        ai_output, ai_assisted = self._run_ai_layer(
            event, detections, kb_entries, severity_floor, confidence_floor
        )

        primary_kb = kb_entries[0]
        return SecurityAnalysis(
            schema_version=self.SCHEMA_VERSION,
            event_id=event.event_id,
            threat=self._pick_str(ai_output.get("threat"), detections[0].title),
            vulnerability=self._pick_str(
                ai_output.get("vulnerability"), primary_kb["vulnerability"]
            ),
            cve=cve,
            cwe=cwe,
            # Severity is a floor set by deterministic rules -- the AI may
            # not downgrade it, only agree or (implicitly, via its own
            # separate escalation workflow) flag for human upgrade.
            severity=severity_floor,
            confidence=confidence_floor,
            evidence=evidence,
            impact=self._pick_str(ai_output.get("impact"), primary_kb["impact_baseline"]),
            immediate_containment=self._pick_str(
                ai_output.get("immediate_containment"), primary_kb["containment_baseline"]
            ),
            recommended_remediation=self._pick_list(
                ai_output.get("recommended_remediation"), primary_kb["remediation_baseline"]
            ),
            mitre_attack=mitre,
            verification=self._pick_str(
                ai_output.get("verification"), primary_kb["verification_baseline"]
            ),
            risk_score=risk_score,
            risk_level=risk_level(risk_score),
            ai_assisted=ai_assisted,
            source_rules=[d.rule_id for d in detections],
        )

    # ---- AI layer (isolated so failures can't break the deterministic path) ----

    def _run_ai_layer(
        self,
        event: SecurityEvent,
        detections: list[Detection],
        kb_entries: list[dict[str, Any]],
        severity_floor: str,
        confidence_floor: int,
    ) -> tuple[dict[str, Any], bool]:
        if self.ai_fn is None:
            return {}, False

        context = self._build_ai_context(
            event, detections, kb_entries, severity_floor, confidence_floor
        )
        try:
            result = self.ai_fn(context)
        except Exception:
            # AI is additive only -- never let a provider error break
            # the deterministic analysis.
            return {}, False

        if not isinstance(result, dict):
            return {}, False
        return result, True

    @staticmethod
    def _build_ai_context(
        event: SecurityEvent,
        detections: list[Detection],
        kb_entries: list[dict[str, Any]],
        severity_floor: str,
        confidence_floor: int,
    ) -> dict[str, Any]:
        return {
            "event": {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "source": event.source,
                "message": event.message,
                "metadata": event.metadata,
            },
            "detections": [
                {"rule_id": d.rule_id, "title": d.title, "reason": d.reason}
                for d in detections
            ],
            "knowledge_base": kb_entries,
            "severity_floor": severity_floor,
            "confidence_floor": confidence_floor,
            "instructions": (
                "You are assisting a security analyst who already has "
                "confirmed detections. CVE, CWE, MITRE ATT&CK technique, "
                "and evidence are already determined deterministically and "
                "are not yours to change or invent. Your job is limited to: "
                "explaining the threat and vulnerability in plain language, "
                "describing business impact, and writing practical "
                "immediate-containment, remediation, and verification "
                "guidance grounded only in the provided detections and "
                "knowledge_base. Never report a severity below "
                "severity_floor. Respond ONLY as JSON with keys: threat, "
                "vulnerability, impact, immediate_containment, "
                "recommended_remediation (array of strings), verification."
            ),
        }

    # ---- deterministic merge helpers ----

    @staticmethod
    def _severity_floor(detections: list[Detection]) -> str:
        return max(detections, key=lambda d: SEVERITY_RANK.get(d.severity, 0)).severity

    @staticmethod
    def _confidence_floor(detections: list[Detection]) -> int:
        return max(CONFIDENCE_FLOOR_BY_LEVEL.get(d.confidence, 50) for d in detections)

    @staticmethod
    def _first_non_default(entries: list[dict[str, Any]], key: str) -> str:
        for e in entries:
            if e.get(key) and e[key] != DEFAULT_ENTRY[key]:
                return e[key]
        return entries[0].get(key, DEFAULT_ENTRY[key]) if entries else DEFAULT_ENTRY[key]

    @staticmethod
    def _merge_mitre(entries: list[dict[str, Any]]) -> list[dict[str, str]]:
        merged: dict[str, dict[str, str]] = {}
        for e in entries:
            for technique in e.get("mitre_attack", []):
                merged[technique["id"]] = technique
        return list(merged.values())

    @staticmethod
    def _pick_str(ai_value: Any, fallback: str) -> str:
        if isinstance(ai_value, str) and ai_value.strip():
            return ai_value.strip()
        return fallback

    @staticmethod
    def _pick_list(ai_value: Any, fallback: list[str]) -> list[str]:
        if (
            isinstance(ai_value, list)
            and ai_value
            and all(isinstance(x, str) and x.strip() for x in ai_value)
        ):
            return ai_value
        return fallback
