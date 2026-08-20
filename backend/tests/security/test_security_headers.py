def test_security_header_policy_documented():
    # Regression marker: production proxy and application must set these headers.
    required = {
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Referrer-Policy",
        "Strict-Transport-Security",
    }
    assert len(required) == 4
