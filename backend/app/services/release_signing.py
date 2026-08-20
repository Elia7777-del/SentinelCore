"""
Signed release manifest verification foundation.

Production design:
- The trusted public key must be provisioned out-of-band.
- Never accept a public key supplied by the update payload itself.
- Verify the signature over canonical JSON bytes.
"""
import base64
import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

def canonical_manifest(manifest: dict) -> bytes:
    payload = {k: v for k, v in manifest.items() if k != "signature"}
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()

def verify_release_manifest(manifest: dict, public_key_pem: bytes) -> bool:
    signature = manifest.get("signature")
    if not signature:
        return False

    try:
        signature_bytes = base64.b64decode(signature, validate=True)
        public_key = serialization.load_pem_public_key(public_key_pem)
        if not isinstance(public_key, Ed25519PublicKey):
            return False
        public_key.verify(signature_bytes, canonical_manifest(manifest))
        return True
    except Exception:
        return False
