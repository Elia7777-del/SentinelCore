#!/usr/bin/env bash
set -euo pipefail
: "${SENTINELCORE_API:?Set SENTINELCORE_API}"
: "${SENTINELCORE_ENROLLMENT_TOKEN:?Set SENTINELCORE_ENROLLMENT_TOKEN}"

echo "SentinelCore Linux agent enrollment"
echo "API: ${SENTINELCORE_API}"
echo "Enrollment token supplied."
echo "Production requirement: install a signed, independently tested agent package."
