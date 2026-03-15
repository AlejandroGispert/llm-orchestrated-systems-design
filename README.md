# Agentic Design Lab

LLM-orchestrated multi-disciplinary design workflow. Autonomous evolving agent that iteratively proposes, simulates, verifies, and documents reusable orbital vehicle concepts. Runs every 4–8 hours via GitHub Actions: reads design state, plans improvements, implements, verifies, and commits.

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
│   ├── IDENTITY.md               # Agent constitution (immutable)
│   ├── JOURNAL.md                # Session log
│   ├── LEARNINGS.md              # Design lessons
│   ├── TAKEAWAYS.md    # Architecture & domain takeaways
│   ├── SETUP.md                  # Setup & code structure guide
│   └── IMPLEMENTATION_STEPS.md   # Implementation phases
├── designs/                       # Design documents
└── simulations/                   # Trajectory, structural, thermal scripts
```

## Run Locally

```bash
ANTHROPIC_API_KEY=sk-... ./scripts/evolve.sh
```

Requires: Python 3.11+, `gh` CLI. See [docs/SETUP.md](docs/SETUP.md).

## License

MIT
