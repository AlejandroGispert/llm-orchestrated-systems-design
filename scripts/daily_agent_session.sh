#!/bin/bash
# scripts/evolve.sh — One evolution cycle for the llm-orchestrated-systems-design agent.
# Runs every 4–8 hours via GitHub Actions or manually.
#
# Usage:
#   ANTHROPIC_API_KEY=sk-... ./scripts/evolve.sh   # cloud (paid)
#   LLM_PROVIDER=ollama ./scripts/evolve.sh        # local Ollama (free)
#
# Environment:
#   ANTHROPIC_API_KEY  — required if not using Ollama
#   LLM_PROVIDER       — set to "ollama" for local/free LLM (no API key needed)
#   OLLAMA_MODEL       — optional; default llama3.1 (only if LLM_PROVIDER=ollama)
#   AGENT_RUNTIME      — "langgraph" (default) or "hermes"
#   HERMES_MODEL       — optional Hermes model id (used when AGENT_RUNTIME=hermes)
#   REPO               — GitHub repo (e.g. owner/llm-orchestrated-systems-design)
#   GH_TOKEN           — for gh CLI (issues, push)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO="${REPO:-}"
# Load .env so local runs pick up API keys without manual export.
[ -f "$REPO_ROOT/.env" ] && set -a && source "$REPO_ROOT/.env" && set +a
DATE=$(date +%Y-%m-%d)
SESSION_TIME=$(date +%H:%M)

# Day count (days since project start)
# Use BIRTH_DATE if set, otherwise default to project start date.
BIRTH_DATE="${BIRTH_DATE:-2026-03-15}"
if date -j &>/dev/null 2>&1; then
  DAY=$(( ($(date +%s) - $(date -j -f "%Y-%m-%d" "$BIRTH_DATE" +%s)) / 86400 ))
else
  DAY=$(( ($(date +%s) - $(date -d "$BIRTH_DATE" +%s)) / 86400 ))
fi

echo "=== Agentic Design Lab — Day $DAY ($DATE $SESSION_TIME) ==="
echo ""

# ── Step 1: Ensure identity files exist ──
mkdir -p "$REPO_ROOT/designs" "$REPO_ROOT/simulations" "$REPO_ROOT/specs" "$REPO_ROOT/skills" "$REPO_ROOT/docs"
for f in IDENTITY.md JOURNAL.md LEARNINGS.md; do
  if [ ! -f "$REPO_ROOT/docs/$f" ]; then
    echo "# $f" > "$REPO_ROOT/docs/$f"
    echo "" >> "$REPO_ROOT/docs/$f"
    echo "*(placeholder — edit with your agent's identity and memory)*" >> "$REPO_ROOT/docs/$f"
  fi
done

# ── Step 2: Run agent session (Python agent) ──
echo "→ Running agent session..."
cd "$REPO_ROOT"
# Prefer venv Python (avoids macOS "externally-managed-environment")
PYTHON="${REPO_ROOT}/.venv/bin/python"
[ -x "$PYTHON" ] || PYTHON="python3"
AGENT_RUNTIME="${AGENT_RUNTIME:-langgraph}"
if [ "$AGENT_RUNTIME" = "hermes" ]; then
  echo "  runtime: hermes"
  $PYTHON -m agent.evolve_hermes \
    --day "$DAY" \
    --date "$DATE" \
    --time "$SESSION_TIME" \
    || true
else
  echo "  runtime: langgraph"
  $PYTHON -m agent.evolve \
    --day "$DAY" \
    --date "$DATE" \
    --time "$SESSION_TIME" \
    || true
fi

# ── Step 3: Push if we have commits ──
if [ -n "${GH_TOKEN:-}" ] && [ -n "${REPO:-}" ]; then
  if ! git diff --quiet HEAD origin/main 2>/dev/null; then
    echo "→ Pushing..."
    git push "https://x-access-token:${GH_TOKEN}@github.com/${REPO}.git" HEAD:main 2>/dev/null || echo "  Push skipped (check token/perms)"
  fi
fi

echo ""
echo "=== Day $DAY complete ==="
