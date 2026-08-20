# Edge Security

Place SentinelCore behind a production API gateway/WAF/reverse proxy.

Recommended limits:
- Login: strict per-IP and per-account rate limits.
- Agent ingestion: per-agent and per-organization quotas.
- General API: per-user and per-IP limits.
- Large payload limits.
- Request timeouts.
- Connection limits.

The repository includes an Nginx template. Exact limits must be tuned after load testing.
Do not consider a reverse proxy configuration alone to be a complete WAF.
