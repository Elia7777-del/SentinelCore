"""
Backend integration for the AI Security Analyst.

Wires the deterministic sentinelcore.analysis.AISecurityAnalyst to:
  - the persisted SecurityEvent DB model (adapter),
  - per-organization AI provider credentials and detection tuning
    (falling back to deployment-wide defaults), and
  - an optional external AI provider for the narrative layer only.

Resolution order for AI credentials, per org:
  1. The org's own ai_api_url / ai_api_key_encrypted, if ai_enabled and set.
  2. The deployment-wide SENTINELCORE_AI_API_URL / SENTINELCORE_AI_API_KEY.
  3. Neither configured -> AI layer is a no-op; analysis still succeeds
     using only deterministic detections. See sentinelcore.analysis.analyst
     for why that fallback is a hard requirement: the AI is never allowed
     to be the only source of a finding, a CVE/CWE, or a severity level.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any

import requests

from app.core.config import settings
from app.models.event import SecurityEvent as DBSecurityEvent
from app.models.tenant import Organization
from app.services.secrets_crypto import SecretDecryptionFailed, decrypt_secret
from sentinelcore.analysis.analyst import AISecurityAnalyst, SecurityAnalysis
from sentinelcore.core.models import SecurityEvent as CoreSecurityEvent
from sentinelcore.detection.engine import DetectionConfig, DetectionEngine

logger = logging.getLogger("sentinelcore.ai_security_analyst")

_DB_SEVERITY_TO_LABEL = {
    1: "Info", 2: "Info", 3: "Low", 4: "Low",
    5: "Medium", 6: "Medium", 7: "High", 8: "High",
    9: "Critical", 10: "Critical",
}

# Only these keys ever flow from the AI provider into the analysis.
# Anything else the model returns -- including an attempted "severity"
# or "cwe" override -- is silently dropped before it reaches
# AISecurityAnalyst. This is enforced here AND is redundant with the
# analyst itself never reading those keys; two independent layers.
_ALLOWED_AI_FIELDS = {
    "threat",
    "vulnerability",
    "impact",
    "immediate_containment",
    "recommended_remediation",
    "verification",
}


@dataclass(frozen=True)
class _ResolvedAIProvider:
    api_url: str
    api_key: str
    model: str


def _resolve_ai_provider(org: Organization | None) -> _ResolvedAIProvider | None:
    """Picks an org's own AI credentials if configured and enabled,
    otherwise the deployment-wide default. Returns None if neither is
    usable -- callers treat that as "AI layer disabled"."""
    if org is not None and org.ai_enabled and org.ai_api_url and org.ai_api_key_encrypted:
        try:
            key = decrypt_secret(org.ai_api_key_encrypted)
        except SecretDecryptionFailed:
            logger.error(
                "Could not decrypt AI API key for org %s -- check "
                "SENTINELCORE_ENCRYPTION_KEY hasn't changed. Falling back "
                "to the deployment default provider.",
                org.id,
            )
        else:
            if key:
                return _ResolvedAIProvider(
                    api_url=org.ai_api_url,
                    api_key=key,
                    model=org.ai_model or settings.ai_model,
                )

    api_url = (settings.ai_api_url or "").strip()
    api_key = (settings.ai_api_key or "").strip()
    if api_url and api_key:
        return _ResolvedAIProvider(api_url=api_url, api_key=api_key, model=settings.ai_model)

    return None


def _db_event_to_core_event(row: DBSecurityEvent) -> CoreSecurityEvent:
    try:
        payload = json.loads(row.payload_json) if row.payload_json else {}
    except (TypeError, ValueError):
        payload = {}
    if not isinstance(payload, dict):
        payload = {}

    return CoreSecurityEvent(
        event_id=row.id,
        timestamp=row.received_at.isoformat() if row.received_at else "",
        source=row.source or "unknown",
        event_type=row.event_type,
        severity=_DB_SEVERITY_TO_LABEL.get(row.severity, "Info"),
        message=row.summary or "",
        metadata=payload,
    )


def _detection_config_for_org(org: Organization | None) -> DetectionConfig:
    if org is None or not org.detection_config_json:
        return DetectionConfig()
    try:
        parsed = json.loads(org.detection_config_json)
    except ValueError:
        logger.warning("Org %s has invalid detection_config_json; using defaults.", org.id)
        return DetectionConfig()
    return DetectionConfig.from_dict(parsed)


def _make_ai_fn(provider: _ResolvedAIProvider | None):
    if provider is None:
        return None

    def ai_fn(context: dict[str, Any]) -> dict[str, Any] | None:
        prompt = f"{context['instructions']}\n\nContext (JSON):\n{json.dumps(context, default=str)}"
        headers = {"Authorization": f"Bearer {provider.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": provider.model,
            "max_tokens": 800,
            "messages": [{"role": "user", "content": prompt}],
        }
        try:
            response = requests.post(provider.api_url, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as exc:
            logger.warning("AI security analyst provider call failed: %s", exc)
            return None

        text = _extract_text(data)
        if not text:
            return None

        parsed = _extract_json_object(text)
        if not isinstance(parsed, dict):
            logger.warning("AI security analyst provider returned non-JSON output")
            return None

        return {k: v for k, v in parsed.items() if k in _ALLOWED_AI_FIELDS}

    return ai_fn


def _extract_text(data: Any) -> str:
    if isinstance(data, dict):
        # Anthropic Messages API shape: {"content": [{"type": "text", "text": ...}, ...]}
        content = data.get("content")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    return str(block.get("text", ""))
        for key in ("text", "response", "output"):
            value = data.get(key)
            if isinstance(value, str):
                return value
    return ""


def _extract_json_object(text: str) -> Any:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(text[start : end + 1])
    except ValueError:
        return None


def get_analyst(org: Organization | None = None) -> AISecurityAnalyst:
    provider = _resolve_ai_provider(org)
    detection_config = _detection_config_for_org(org)
    return AISecurityAnalyst(
        detection_engine=DetectionEngine(config=detection_config),
        ai_fn=_make_ai_fn(provider),
    )


def analyze_event(
    row: DBSecurityEvent,
    org: Organization | None = None,
    asset_criticality: str = "Medium",
) -> dict[str, Any] | None:
    """Run detection -> intelligence -> AI -> risk scoring for a
    persisted event, using the owning organization's AI credentials and
    detection tuning if configured. Returns None if no detection rule
    fired (nothing to report), or a fully-populated analysis dict
    otherwise."""
    core_event = _db_event_to_core_event(row)
    analysis: SecurityAnalysis | None = get_analyst(org).analyze(
        core_event, asset_criticality=asset_criticality
    )
    return analysis.to_dict() if analysis else None
