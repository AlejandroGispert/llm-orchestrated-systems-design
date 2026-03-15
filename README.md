# Agentic Design Lab

LLM-orchestrated multi-disciplinary design workflow. Autonomous evolving agent that iteratively proposes, simulates, verifies, and documents a design concept. Runs every 4–8 hours (GitHub Actions or local cron): reads design state, plans improvements, implements, verifies, and commits.

**Positioning:** Research platform exploring how agentic AI systems can assist early-stage multidisciplinary conceptual design. Closed-loop design → simulate → evaluate → revise.

## How It Works

- **Schedule:** Runs every 4 hours (cron: `0 */4 * * *`)
- **Loop:** Plan → implement → simulate → verify → journal → push
- **Scope:** Design docs, simulations, specs 

## Project Structure

```
├── .github/workflows/evolve.yml   # Scheduled evolution
├── scripts/evolve.sh              # Evolution pipeline
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

**Option A — Cloud (Anthropic, paid)**  
```bash
ANTHROPIC_API_KEY=sk-... ./scripts/evolve.sh
```

**Option B — Local LLM (free, no API key)**  
```bash
# Install Ollama + pull a model: https://ollama.com → e.g. ollama pull llama3.1
LLM_PROVIDER=ollama ./scripts/evolve.sh
```

**Option C — Cursor CLI (no Anthropic key)**  
Uses your Cursor subscription. One run: `./scripts/run-evolve-cursor.sh`. Every 4 hours: `0 */4 * * * /path/to/scripts/run-evolve-cron.sh` in crontab. See [docs/SETUP.md](docs/SETUP.md) §6.

To run every 4 hours on your machine (no GitHub Actions, no Anthropic): use a **cron job** with Option B (Ollama) or Option C (Cursor CLI). See [docs/SETUP.md](docs/SETUP.md).

Requires: Python 3.11+, `gh` CLI (optional, for push). See [docs/SETUP.md](docs/SETUP.md).

## License

MIT
