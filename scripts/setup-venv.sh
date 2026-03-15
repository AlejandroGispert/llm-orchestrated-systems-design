#!/bin/bash
# Create venv and install deps. Use this on macOS when pip gives "externally-managed-environment".
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
echo "Done. Activate with: source .venv/bin/activate"
echo "Or run evolve.sh — it will use .venv automatically."
