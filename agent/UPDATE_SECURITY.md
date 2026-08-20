# SentinelCore Agent Update Security

Production agents should not blindly execute downloaded updates.

Required release design:
1. Build agent package in a controlled CI environment.
2. Generate a cryptographic SHA-256 digest.
3. Sign the release manifest using an organization-controlled signing key.
4. Publish the package and signature through an authenticated distribution service.
5. Agent embeds the trusted public verification key.
6. Agent verifies signature and package digest before installation.
7. Reject unsigned, altered, expired or downgraded packages.
8. Keep an emergency rollback package.
9. Record update result in the central audit system.

The current repository documents the required control; a production updater should be implemented
and tested before enabling remote automatic updates.
