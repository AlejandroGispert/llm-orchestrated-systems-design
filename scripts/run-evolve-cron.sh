#!/bin/bash
# Cron entry point: run one evolution with Cursor CLI agent, then log.
# Schedule every 4 hours: 0 */4 * * * /path/to/llm-orchestrated-systems-design/scripts/run-evolve-cron.sh
#
# Ensure Cursor CLI is installed and authenticated (CURSOR_API_KEY in .env).
# Optional: GH_TOKEN and REPO in .env to push after each run.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Cron has a minimal PATH; add common Cursor CLI locations so `agent` is found
export PATH="/usr/local/bin:/opt/homebrew/bin:$HOME/.local/bin:/Applications/Cursor.app/Contents/Resources/app/bin:$PATH"

# Load .env so CURSOR_API_KEY (and optional GH_TOKEN, REPO) are set for cron
[ -f "$REPO_ROOT/.env" ] && set -a && source "$REPO_ROOT/.env" && set +a
mkdir -p "$REPO_ROOT/logs"
LOG="$REPO_ROOT/logs/evolve.log"

# Portable timestamp (works on macOS and Linux)
echo "--- $(date '+%Y-%m-%dT%H:%M:%S%z') ---" >> "$LOG"
"$SCRIPT_DIR/run-evolve-cursor.sh" >> "$LOG" 2>&1
echo "" >> "$LOG"
