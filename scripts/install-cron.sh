#!/bin/bash
# One-time setup: add the every-4-hours cron job and ensure logs/ exists.
# Run from repo root: ./scripts/install-cron.sh

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CRON_SCRIPT="$REPO_ROOT/scripts/run-evolve-cron.sh"
CRON_LINE="0 */4 * * * $CRON_SCRIPT"

# Ensure logs dir and log file exist so tail works
mkdir -p "$REPO_ROOT/logs"
touch "$REPO_ROOT/logs/evolve.log"

# Add to crontab (keep existing lines) — use temp file so it works when no crontab exists yet (e.g. macOS)
EXISTING=$(crontab -l 2>/dev/null || true)
if echo "$EXISTING" | grep -Fq "$CRON_SCRIPT"; then
  echo "Cron job already installed: $CRON_LINE"
else
  TMP=$(mktemp)
  echo "$EXISTING" | grep -v '^$' > "$TMP" 2>/dev/null || true
  echo "$CRON_LINE" >> "$TMP"
  crontab "$TMP" && rm -f "$TMP" && echo "Installed cron job: $CRON_LINE" || { echo "Failed to install crontab"; rm -f "$TMP"; exit 1; }
fi
echo ""
echo "Verify: crontab -l"
echo "Test run: $CRON_SCRIPT"
echo "Log: tail -f $REPO_ROOT/logs/evolve.log"
