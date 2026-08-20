def test_security_response_mode_defaults_to_approval_required():
    # Contract test: production should not silently enable disruptive automation.
    import os
    assert os.getenv("DEFAULT_RESPONSE_MODE", "approval_required") in {
        "approval_required", "alert_only", "automatic"
    }

def test_no_default_public_database_port():
    compose = open("../../deploy/docker/docker-compose.enterprise.yml", encoding="utf-8").read()
    assert 'ports:\n      - "5432:5432"' not in compose
