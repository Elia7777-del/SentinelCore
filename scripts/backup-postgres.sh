#!/usr/bin/env bash
set -euo pipefail
: "${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD}"
OUT="${1:-backups/sentinelcore-$(date -u +%Y%m%dT%H%M%SZ).dump}"
mkdir -p "$(dirname "$OUT")"
docker compose -f deploy/docker/docker-compose.enterprise.yml exec -T db   pg_dump -U sentinelcore -d sentinelcore -Fc > "$OUT"
echo "Backup written to $OUT"
