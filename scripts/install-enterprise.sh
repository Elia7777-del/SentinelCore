#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [ ! -f .env.production ]; then
  cp .env.production.example .env.production
  echo "Created .env.production. Edit it and set real secrets before continuing."
  exit 1
fi

if grep -q 'REPLACE_WITH' .env.production; then
  echo "ERROR: replace all placeholder production secrets first."
  exit 1
fi

docker compose -f deploy/docker/docker-compose.enterprise.yml up -d --build
echo "SentinelCore enterprise stack started."
