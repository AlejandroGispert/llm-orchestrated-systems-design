# Agentic Design Lab

LLM-orchestrated multi-disciplinary design workflow. Autonomous evolving agent that iteratively proposes, simulates, verifies, and documents a design concept. Can run automatically (GitHub Actions) or locally: reads design state, plans improvements, implements, verifies, and commits.

**Positioning:** Research platform exploring how agentic AI systems can assist early-stage multidisciplinary conceptual design. Closed-loop design → simulate → evaluate → revise.

## Daily Concept Design Agent

- **Workflow:** `.github/workflows/daily_agent.yml`
  - Name: **Daily Concept Design Agent**
  - Schedule: `0 0 * * *` (once per day at 00:00 UTC)
  - Behavior: checks out the repo, installs dependencies, and runs a single evolution cycle via `scripts/daily_agent_session.sh`.
  - Default provider/runtime: `LLM_PROVIDER=anthropic`, `ANTHROPIC_MODEL=claude-sonnet-4-5`, `AGENT_RUNTIME=langgraph`
- **Loop:** Plan → implement → simulate (optional) → verify → journal → commit → push
- **Scope:** Design docs (`designs/`), simulations (`simulations/`), specs (`specs/`), and agent memory docs (`docs/`).

## Project Structure

```
├── .github/workflows/daily_agent.yml   # Daily Concept Design Agent workflow
├── scripts/daily_agent_session.sh      # Daily agent pipeline
├── docs/                          # Documentation
│   ├── IDENTITY.md                # Agent constitution (immutable)
│   ├── JOURNAL.md                 # Session log
│   ├── LEARNINGS.md               # Design lessons
│   ├── TAKEAWAYS.md               # Architecture & domain takeaways
│   ├── SETUP.md                   # Setup & code structure guide
│   └── IMPLEMENTATION_STEPS.md    # Implementation phases
├── designs/                       # Design documents
└── simulations/                   # Trajectory, structural, thermal scripts
```

## Run Locally

```bash
cd /Users/alejandrolivemusicmac/Documents/1_CODE_PROJECTS/llm-orchestrated-systems-design
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Load environment (API keys, REPO/GH_TOKEN if used)
set -a && . .env && set +a

# Run one daily agent session (same path used by GitHub Actions)
AGENT_RUNTIME=langgraph \
LLM_PROVIDER=anthropic \
ANTHROPIC_MODEL=claude-sonnet-4-5 \
./scripts/daily_agent_session.sh
```

### Runtime options

- `AGENT_RUNTIME=langgraph` (default): uses `agent/evolve.py`
- `AGENT_RUNTIME=hermes`: uses `agent/evolve_hermes.py`
  - Install Hermes dependencies in isolated env:
    ```bash
    python3.11 -m venv .venv-hermes
    .venv-hermes/bin/pip install -r requirements-hermes.txt
    ```

### Provider options

- Anthropic (default): set `ANTHROPIC_API_KEY`
- Gemini: set `LLM_PROVIDER=gemini` and `GEMINI_API_KEY`
- Ollama (local): set `LLM_PROVIDER=ollama` and optional `OLLAMA_MODEL`

### Troubleshooting

- `permission denied: ./scripts/daily_agent_session.sh`
  - Run: `chmod +x scripts/daily_agent_session.sh`
- Anthropic billing/auth errors
  - Verify the key belongs to a funded Anthropic API workspace.
- If local Python analysis points to stale `.venv` paths after env migration
  - Restart Python language server / IDE window.

- Requires: Python 3.11+, `gh` CLI (optional, for push). See [docs/SETUP.md](docs/SETUP.md).

## License

MIT
