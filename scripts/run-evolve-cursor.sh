#!/bin/bash
# One evolution cycle using Cursor CLI agent (headless). No Anthropic API key — uses your Cursor subscription.
#
# Usage:
#   ./scripts/run-evolve-cursor.sh
#   Or from cron: use scripts/run-evolve-cron.sh which calls this and logs.
#
# Environment:
#   CURSOR_API_KEY  — set if not already authenticated (see cursor.com/docs/cli)
#   REPO            — optional; GitHub repo (owner/name) for push
#   GH_TOKEN        — optional; for git push after commit
#   BIRTH_DATE      — optional; YYYY-MM-DD for day count (default 2025-03-15)
#
# Uses --model auto so Cursor picks a model available in your pool (avoids slow-pool errors).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
# Load .env so CURSOR_API_KEY is available (manual run or when cron doesn't source it)
[ -f "$REPO_ROOT/.env" ] && set -a && source "$REPO_ROOT/.env" && set +a
DATE=$(date +%Y-%m-%d)
SESSION_TIME=$(date +%H:%M)

BIRTH_DATE="${BIRTH_DATE:-2025-03-15}"
BIRTH_EPOCH=$(date -j -f "%Y-%m-%d" "$BIRTH_DATE" +%s 2>/dev/null || date -d "$BIRTH_DATE" +%s 2>/dev/null)
DAY=$(( ($(date +%s) - BIRTH_EPOCH) / 86400 ))

echo "=== Agentic Design Lab (Cursor CLI) — Day $DAY ($DATE $SESSION_TIME) ==="

# Ensure dirs and placeholder docs exist (same as evolve.sh)
mkdir -p "$REPO_ROOT/designs" "$REPO_ROOT/simulations" "$REPO_ROOT/specs" "$REPO_ROOT/docs"
for f in IDENTITY.md JOURNAL.md LEARNINGS.md; do
  [ -f "$REPO_ROOT/docs/$f" ] || { echo "# $f" > "$REPO_ROOT/docs/$f"; echo "" >> "$REPO_ROOT/docs/$f"; echo "*(placeholder)*" >> "$REPO_ROOT/docs/$f"; }
done

cd "$REPO_ROOT"

PROMPT="You are an aerospace conceptual design agent. Today is Day $DAY ($DATE $SESSION_TIME).

Read these files: docs/IDENTITY.md, docs/JOURNAL.md, docs/LEARNINGS.md, docs/TAKEAWAYS.md. List the contents of designs/.

Your task: Make ONE focused improvement. Choose one of:
- Add or refine a design document in designs/
- Create designs/concept-v1.md if designs/ is empty
- Prepend a short entry to docs/JOURNAL.md for this session
- Update docs/LEARNINGS.md if you learned something
- Add a requirement or trade in specs/

Rules:
- One focused change only.
- Only modify: designs/, simulations/, specs/, docs/JOURNAL.md, docs/LEARNINGS.md.
- Never modify: docs/IDENTITY.md, .github/, scripts/, agent/.
- When done, run in the repo root: git add -A && git commit -m 'Day $DAY ($SESSION_TIME): <brief description>'"

if ! command -v agent &>/dev/null; then
  echo "Error: Cursor CLI 'agent' not found. Install: curl https://cursor.com/install -fsS | bash" >&2
  exit 1
fi

# Use --model auto so Cursor picks an available model (avoids "not available in the slow pool" errors)
agent -p --force --model auto "$PROMPT" || true

# Optional push: set GH_TOKEN and REPO (e.g. in .env) to push after each run
REPO="${REPO:-}"
if [ -z "${GH_TOKEN:-}" ] || [ -z "$REPO" ]; then
  echo "  (Push skipped: set GH_TOKEN and REPO=owner/repo in .env to enable)"
elif git diff --quiet HEAD origin/main 2>/dev/null; then
  echo "  (Push skipped: no new commits to push)"
else
  echo "→ Pushing..."
  if git push "https://x-access-token:${GH_TOKEN}@github.com/${REPO}.git" HEAD:main 2>/dev/null; then
    echo "  Pushed to origin/main"
  else
    echo "  Push failed (check GH_TOKEN, REPO, and branch name)"
  fi
fi

echo "=== Day $DAY complete ==="
