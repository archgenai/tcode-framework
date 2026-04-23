#!/usr/bin/env bash
# install-hooks.sh — Install git hooks into a project's .git/hooks directory.
#
# Usage (run from TCode root):
#   bash devops/scripts/install-hooks.sh projects/budget-tracker-poc
#   bash devops/scripts/install-hooks.sh projects/patient-health-analyzer
#
# Installs:
#   commit-msg  — validates Conventional Commits format
#   pre-push    — runs test suite before any push

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_SRC="$SCRIPT_DIR/../hooks"

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
    echo "Usage: bash devops/scripts/install-hooks.sh <project-path>"
    echo "  e.g. bash devops/scripts/install-hooks.sh projects/budget-tracker-poc"
    exit 1
fi

GIT_HOOKS_DIR="$TARGET/.git/hooks"

if [[ ! -d "$TARGET/.git" ]]; then
    echo "ERROR: $TARGET is not a git repository. Run: git init $TARGET"
    exit 1
fi

mkdir -p "$GIT_HOOKS_DIR"

for hook in commit-msg pre-push; do
    src="$HOOKS_SRC/$hook"
    dst="$GIT_HOOKS_DIR/$hook"
    cp "$src" "$dst"
    chmod +x "$dst"
    echo "Installed: $dst"
done

echo ""
echo "Git hooks installed in $GIT_HOOKS_DIR"
echo ""
echo "Also run the following to install pre-commit framework hooks:"
echo "  cd $TARGET && pip install pre-commit && pre-commit install"
