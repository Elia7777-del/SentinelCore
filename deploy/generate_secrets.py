import secrets
print("SENTINELCORE_SECRET_KEY=" + secrets.token_urlsafe(64))
print("POSTGRES_PASSWORD=" + secrets.token_urlsafe(32))
