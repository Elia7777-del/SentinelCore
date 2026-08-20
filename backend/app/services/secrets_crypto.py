"""
Secret-at-rest encryption for per-organization credentials (e.g. an org's
own AI provider API key).

Uses Fernet (AES-128-CBC + HMAC, via the `cryptography` package already a
project dependency) with a single master key from settings. The master
key must never be stored in the database -- only in the deployment's
environment/secret manager -- otherwise a DB compromise would also
compromise every tenant's stored secrets.

If SENTINELCORE_ENCRYPTION_KEY is not configured, encrypt/decrypt raise a
clear error instead of silently storing plaintext or silently failing.
"""
from __future__ import annotations

from cryptography.fernet import Fernet, InvalidToken

from app.core.config import settings


class SecretEncryptionNotConfigured(RuntimeError):
    pass


class SecretDecryptionFailed(RuntimeError):
    pass


def _fernet() -> Fernet:
    key = (settings.encryption_key or "").strip()
    if not key:
        raise SecretEncryptionNotConfigured(
            "SENTINELCORE_ENCRYPTION_KEY is not set. Generate one with "
            "generate_encryption_key() and set it in the environment before "
            "storing any org-level secrets."
        )
    try:
        return Fernet(key.encode())
    except (ValueError, TypeError) as exc:
        raise SecretEncryptionNotConfigured(
            "SENTINELCORE_ENCRYPTION_KEY is set but is not a valid Fernet key. "
            "Generate one with generate_encryption_key()."
        ) from exc


def generate_encryption_key() -> str:
    """Generates a new Fernet key suitable for SENTINELCORE_ENCRYPTION_KEY.
    Run once per deployment and store the result in your secret manager --
    rotating it invalidates every previously-encrypted org secret."""
    return Fernet.generate_key().decode()


def encrypt_secret(plaintext: str) -> str:
    if not plaintext:
        return ""
    return _fernet().encrypt(plaintext.encode()).decode()


def decrypt_secret(token: str) -> str:
    if not token:
        return ""
    try:
        return _fernet().decrypt(token.encode()).decode()
    except InvalidToken as exc:
        raise SecretDecryptionFailed(
            "Stored secret could not be decrypted -- it may have been "
            "encrypted with a different SENTINELCORE_ENCRYPTION_KEY."
        ) from exc
