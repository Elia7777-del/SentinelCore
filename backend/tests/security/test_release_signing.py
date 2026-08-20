import base64
import json
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from app.services.release_signing import canonical_manifest, verify_release_manifest

def test_release_signature_verifies():
    private = Ed25519PrivateKey.generate()
    public = private.public_key()
    manifest = {"version": "8.0.0", "sha256": "abc123"}
    signature = private.sign(canonical_manifest(manifest))
    manifest["signature"] = base64.b64encode(signature).decode()

    public_pem = public.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    assert verify_release_manifest(manifest, public_pem)

def test_tampered_release_is_rejected():
    private = Ed25519PrivateKey.generate()
    public = private.public_key()
    manifest = {"version": "8.0.0", "sha256": "abc123"}
    manifest["signature"] = base64.b64encode(
        private.sign(canonical_manifest(manifest))
    ).decode()
    manifest["sha256"] = "tampered"

    public_pem = public.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    assert not verify_release_manifest(manifest, public_pem)
