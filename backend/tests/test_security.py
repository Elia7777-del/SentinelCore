from app.services.security import hash_token, verify_token

def test_token_hash_roundtrip():
    token = "example-token"
    hashed = hash_token(token)
    assert verify_token(token, hashed)
    assert not verify_token("wrong-token", hashed)
