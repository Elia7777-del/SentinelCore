# SentinelCore Deployment Quick Start

## Local development

1. Copy `.env.example` to `.env`.
2. Replace all placeholder secrets.
3. Start the API and database:

```bash
docker compose up --build
```

4. Open the API documentation at:

```text
http://localhost:8000/docs
```

## Remote deployment

For a real server:

1. Deploy on a hardened Linux host or managed container platform.
2. Keep PostgreSQL private.
3. Put an HTTPS reverse proxy/API gateway in front of the API.
4. Configure DNS.
5. Install a trusted TLS certificate.
6. Configure firewall/WAF rules.
7. Set strong random secrets through a secret manager.
8. Provision an agent identity/token for each organization/device group.
9. Test ingestion.
10. Enable backups, monitoring and disaster recovery.

## Agent configuration

Set:

```text
SENTINEL_SERVER_URL=https://your-approved-sentinelcore-domain
SENTINEL_AGENT_TOKEN=...
SENTINEL_VERIFY_TLS=true
```

Then run the reference agent from the `agent` directory.

Do not use placeholder tokens, development secrets, or HTTP on the public Internet.
