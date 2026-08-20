#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../web"
python3 -m http.server "${PORT:-8080}" --bind 127.0.0.1
