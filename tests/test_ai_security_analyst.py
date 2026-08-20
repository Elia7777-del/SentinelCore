from sentinelcore.analysis.analyst import AISecurityAnalyst
from sentinelcore.collectors.events import normalize_event


def _credential_stuffing_event():
    return normalize_event(
        {
            "id": "evt-1",
            "type": "authentication",
            "message": "Multiple failed login attempts followed by a successful login",
            "metadata": {"failed_attempts": 9, "outcome": "success"},
        },
        source="test",
    )


def test_deterministic_analysis_without_ai_matches_example_scenario():
    analyst = AISecurityAnalyst()  # no ai_fn -> pure deterministic path
    analysis = analyst.analyze(_credential_stuffing_event())

    assert analysis is not None
    assert analysis.ai_assisted is False
    assert analysis.cwe == "CWE-307"
    assert analysis.cve == "N/A"
    assert analysis.severity == "High"
    assert {"id": "T1110", "name": "Brute Force"} in analysis.mitre_attack
    assert any(t["id"] == "T1110.004" for t in analysis.mitre_attack)
    assert "CRED-001" in analysis.source_rules
    assert analysis.evidence  # deterministic evidence always present
    assert 0 <= analysis.risk_score <= 100


def test_no_detection_returns_none():
    analyst = AISecurityAnalyst()
    benign = normalize_event({"id": "evt-2", "type": "info", "message": "user logged in"}, source="test")
    assert analyst.analyze(benign) is None


def test_ai_cannot_downgrade_severity_or_invent_cwe():
    def rogue_ai(context):
        return {
            "threat": "Something else entirely",
            "vulnerability": "Made up vulnerability",
            "impact": "low impact, ignore this",
            "immediate_containment": "no action needed",
            "recommended_remediation": ["do nothing"],
            "verification": "n/a",
            # Note: no way to pass cve/cwe/severity through ai_fn's
            # output at all -- the schema below just proves that even
            # if it tried, the analyst wouldn't read those fields.
            "severity": "Low",
            "cwe": "CWE-999-FAKE",
        }

    analyst = AISecurityAnalyst(ai_fn=rogue_ai)
    analysis = analyst.analyze(_credential_stuffing_event())

    assert analysis.severity == "High"  # untouched, from the rule floor
    assert analysis.cwe == "CWE-307"    # untouched, from the knowledge base
    assert analysis.ai_assisted is True
    assert analysis.threat == "Something else entirely"  # narrative fields DO flow through


def test_ai_exception_falls_back_to_deterministic_result():
    def broken_ai(context):
        raise RuntimeError("provider timeout")

    analyst = AISecurityAnalyst(ai_fn=broken_ai)
    analysis = analyst.analyze(_credential_stuffing_event())

    assert analysis is not None
    assert analysis.ai_assisted is False
    assert analysis.threat == "Credential Stuffing"  # deterministic fallback title


def test_malformed_ai_response_falls_back_per_field():
    def half_useful_ai(context):
        return {"threat": "Credential stuffing against the login API", "recommended_remediation": "not a list"}

    analyst = AISecurityAnalyst(ai_fn=half_useful_ai)
    analysis = analyst.analyze(_credential_stuffing_event())

    assert analysis.threat == "Credential stuffing against the login API"
    # invalid type -> falls back to the KB baseline list
    assert "Enable MFA." in analysis.recommended_remediation


def test_privileged_auth_failure_backward_compatible():
    analyst = AISecurityAnalyst()
    event = normalize_event({"id": "evt-3", "type": "authentication", "message": "failed login for admin"}, source="test")
    analysis = analyst.analyze(event)
    assert analysis is not None
    assert analysis.severity == "High"
    assert "AUTH-001" in analysis.source_rules
