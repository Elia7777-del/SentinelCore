# SentinelCore v12.0 — Enterprise Deployment Edition

SentinelCore is a defensive cybersecurity platform foundation for authorized organizations.

## v12 focus

This release adds the operational foundation for deploying SentinelCore inside a company:
- Enterprise Docker deployment
- Private PostgreSQL service
- HTTPS reverse-proxy architecture
- Health checks
- Organization onboarding contract
- Agent enrollment workflow
- Linux/Windows onboarding helpers
- Monitoring configuration
- Company onboarding runbook

## Quick start

1. Copy `.env.production.example` to `.env.production`.
2. Replace every placeholder with secure production values.
3. Review `docs/V12_ENTERPRISE_DEPLOYMENT.md`.
4. Run `scripts/install-enterprise.sh`.

Do not expose PostgreSQL directly to the Internet.

## Security boundary

The repository is an engineering/deployment foundation. It does not claim certification,
independent assessment, or guaranteed acceptance by a government or enterprise organization.
Complete the production security gates before protecting real high-value systems.


## v13 production-readiness foundation

Review:
- `docs/PRODUCTION-GO_LIVE_CHECKLIST.md`
- `docs/V13_PRODUCTION_READINESS.md`
- `.env.production.example`
- `deploy/nginx/sentinelcore.conf.example`
- `scripts/backup-postgres.sh`
- `scripts/restore-postgres.sh`

Do not commit production secrets or expose the database directly to the Internet.
