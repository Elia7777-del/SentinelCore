# Production Secrets Management

Do not store production secrets in Git, Docker images, source code, screenshots or chat messages.

Use an approved secret manager/KMS/HSM according to organizational requirements.

Secrets to protect include:
- JWT signing keys
- Database credentials
- Agent bootstrap/provisioning secrets
- Encryption keys
- Third-party API credentials
- Backup keys

Operational requirements:
- Rotation
- Least-privilege access
- Audit logging
- Emergency revocation
- Separate development/test/production secrets
- No hard-coded fallback production secret
