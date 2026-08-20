# Database Migrations

The development code uses SQLAlchemy `create_all()` for simplicity.

For production:
- Adopt Alembic migrations.
- Review every schema change.
- Test upgrades on a copy of production data.
- Keep rollback/restore procedures.
- Never use ad-hoc schema changes against a live database.

The v7 model changes (MFA, refresh sessions, agent expiry) should be migrated with a proper
versioned migration before production use.
