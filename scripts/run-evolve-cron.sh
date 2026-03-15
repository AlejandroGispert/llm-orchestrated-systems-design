#!/bin/bash
# Cron entry point: run one evolution with Cursor CLI agent, then log.
# Schedule every 4 hours: 0 */4 * * * /path/to/llm-orchestrated-systems-design/scripts/run-evolve-cron.sh
#
# Ensure Cursor CLI is installed and authenticated (CURSOR_API_KEY in env or keychain).
# Optional: export GH_TOKEN and REPO in crontab or here to push after each run.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
# Load .env so CURSOR_API_KEY (and optional GH_TOKEN, REPO) are set for cron
[ -f "$REPO_ROOT/.env" ] && set -a && source "$REPO_ROOT/.env" && set +a
mkdir -p "$REPO_ROOT/logs"
LOG="$REPO_ROOT/logs/evolve.log"

echo "--- $(date -Iseconds) ---" >> "$LOG"
"$SCRIPT_DIR/run-evolve-cursor.sh" >> "$LOG" 2>&1
echo "" >> "$LOG"
