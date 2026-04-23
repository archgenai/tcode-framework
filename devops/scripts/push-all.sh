#!/usr/bin/env bash
# push-all.sh — Push current branch to all configured auto-push remotes.
#
# Usage (run from inside any project folder):
#   bash ../../devops/scripts/push-all.sh
#   bash ../../devops/scripts/push-all.sh --include-backup
#
# Or from TCode root:
#   bash devops/scripts/push-all.sh --project budget-tracker-poc

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TCODE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

exec python3 "$TCODE_ROOT/devops/remotes.py" push-all "$@"
