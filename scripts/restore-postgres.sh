#!/usr/bin/env bash
set -euo pipefail
FILE="${1:?Usage: restore-postgres.sh BACKUP.dump}"
test -f "$FILE"
cat "$FILE" | docker compose -f deploy/docker/docker-compose.enterprise.yml exec -T db   pg_restore -U sentinelcore -d sentinelcore --clean --if-exists
echo "Restore completed. Validate application and data integrity before reopening service."
