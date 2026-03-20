"""
Hermes-based design agent runtime for one evolution cycle.

This is an optional runtime selected with:
  AGENT_RUNTIME=hermes ./scripts/daily_agent_session.sh

Dependencies:
  pip install -r requirements-hermes.txt
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_context() -> str:
    docs = REPO_ROOT / "docs"
    identity = (docs / "IDENTITY.md").read_text(encoding="utf-8", errors="replace")
    journal = (docs / "JOURNAL.md").read_text(encoding="utf-8", errors="replace")
    learnings_file = docs / "LEARNINGS.md"
    takeaways_file = docs / "TAKEAWAYS.md"
    learnings = (
        learnings_file.read_text(encoding="utf-8", errors="replace")
        if learnings_file.exists()
        else "(empty)"
    )
    takeaways = (
        takeaways_file.read_text(encoding="utf-8", errors="replace")
        if takeaways_file.exists()
        else "(missing)"
    )
    designs_dir = REPO_ROOT / "designs"
    designs = (
        "\n".join(f"- {f.name}" for f in designs_dir.iterdir() if f.is_file())
        if designs_dir.exists()
        else "(empty)"
    )
    return (
        "=== IDENTITY ===\n"
        f"{identity}\n\n"
        "=== JOURNAL (last ~20 lines) ===\n"
        f"{journal[-3000:] if len(journal) > 3000 else journal}\n\n"
        "=== LEARNINGS ===\n"
        f"{learnings[-2000:] if len(learnings) > 2000 else learnings}\n\n"
        "=== DESIGN BLUEPRINT (TAKEAWAYS.md) ===\n"
        f"{takeaways[:4000]}...\n\n"
        "=== FILES IN designs/ ===\n"
        f"{designs}\n"
    )


def _build_prompt(day: int, date: str, time: str) -> str:
    context = _load_context()
    return f"""You are an aerospace conceptual design agent. Your goal is to evolve toward flight-ready conceptual designs for reusable orbital access.

Today is Day {day} ({date} {time}).

{context}

Task:
- Make ONE focused improvement.
- Prefer JOURNAL's "Next priority" if present.
- Then prepend a short entry to docs/JOURNAL.md.
- End by committing your change.

Allowed paths:
- designs/
- simulations/
- specs/
- docs/JOURNAL.md
- docs/LEARNINGS.md

Forbidden paths:
- docs/IDENTITY.md
- .github/
- scripts/
- agent/

When done, run:
git add -A && git commit -m 'Day {day} ({time}): <brief description>'
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", type=int, required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--time", required=True)
    args = parser.parse_args()

    if not (
        os.environ.get("OPENROUTER_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or os.environ.get("ANTHROPIC_API_KEY")
    ):
        print(
            "Error: Hermes runtime needs one of OPENROUTER_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY.",
            file=sys.stderr,
        )
        sys.exit(1)

    model = os.environ.get("HERMES_MODEL", "google/gemini-2.0-flash-001")
    prompt = _build_prompt(args.day, args.date, args.time)
    hermes_python = os.environ.get(
        "HERMES_PYTHON",
        str(REPO_ROOT / ".venv-hermes" / "bin" / "python"),
    )
    if not Path(hermes_python).exists():
        print(
            "Error: Hermes runtime not found at HERMES_PYTHON/.venv-hermes.\n"
            "Install with: python3.11 -m venv .venv-hermes && .venv-hermes/bin/pip install -r requirements-hermes.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    # Execute Hermes in an isolated subprocess to avoid module-name collisions
    # with this repository's local `agent/` package.
    runner_code = (
        "from run_agent import AIAgent\n"
        "import os\n"
        "agent=AIAgent(model=os.environ['HERMES_MODEL'], quiet_mode=True)\n"
        "print(agent.chat(os.environ['HERMES_PROMPT']))\n"
    )
    env = os.environ.copy()
    env["HERMES_MODEL"] = model
    env["HERMES_PROMPT"] = prompt
    result = subprocess.run(
        [hermes_python, "-c", runner_code],
        cwd="/tmp",
        env=env,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        print("Hermes execution failed:", file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    if result.stdout:
        print(result.stdout.strip())


if __name__ == "__main__":
    main()
