# Setup: Evolution Workflow & Job Application Guide

## What You Have Now

```
llm-orchestrated-systems-design/
├── .github/workflows/evolve.yml   ← Runs every 4 hours
├── agent/evolve.py                ← LangGraph agent
├── scripts/evolve.sh              ← Evolution pipeline
├── docs/
│   ├── TAKEAWAYS.md               ← Design blueprint
│   ├── SETUP.md                   ← This file
│   ├── IDENTITY.md, JOURNAL.md, LEARNINGS.md
│   └── IMPLEMENTATION_STEPS.md
```

## What Needs to Be in Code

### 1. Identity Files (create or edit)

| File | Purpose |
|------|---------|
| `docs/IDENTITY.md` | Mission, constraints, non-negotiables — never modified by agent |
| `docs/JOURNAL.md` | Session log — agent appends entries |
| `docs/LEARNINGS.md` | Design and process lessons — agent updates |

**Minimal IDENTITY.md:**
```markdown


# Rules
- Only modify: designs/, simulations/, specs/, JOURNAL.md, LEARNINGS.md
- Never modify: .github/, scripts/, docs/IDENTITY.md
- One focused change per session
```

### 2. Directory Structure

```
designs/         ← Agent writes design docs here
simulations/     ← Trajectory, structural, thermal scripts (you add later)
specs/           ← Requirements, margins, compliance (you add later)
skills/          ← Optional: custom skills for aerospace domain
```

Create empty dirs if missing:
```bash
mkdir -p designs simulations specs skills
```

### 3. GitHub Secrets (only if using GitHub Actions)

In repo **Settings → Secrets and variables → Actions**, add:

| Secret | Required | Purpose |
|--------|----------|---------|
| `ANTHROPIC_API_KEY` | Yes (if using Actions) | LLM API for the agent |
| `GITHUB_TOKEN` | Auto | Push and issues (provided by Actions) |

### 4. Manual Run (local)

**With Anthropic (paid):**
```bash
ANTHROPIC_API_KEY=sk-... ./scripts/evolve.sh
```

**With Ollama (free, no API key):**
```bash
# Install Ollama from https://ollama.com, then: ollama pull llama3.1
LLM_PROVIDER=ollama ./scripts/evolve.sh
```

### 5. Local cron + Ollama (no Anthropic)

Run the evolution script every 4 hours on your Mac, using local Ollama — no cloud API, no cost.

1. **Install Ollama** and pull a model:
   ```bash
   # From https://ollama.com
   ollama pull llama3.1
   ```

2. **Create a small wrapper** (so cron has the right env and cwd), e.g. `scripts/run-evolve-cron.sh`:
   ```bash
   #!/bin/bash
   cd /Users/you/Documents/1_CODE_PROJECTS/llm-orchestrated-systems-design
   export LLM_PROVIDER=ollama
   # Optional: export GH_TOKEN=... and REPO=owner/repo to push after each run
   ./scripts/evolve.sh >> /tmp/evolve.log 2>&1
   ```
   Make it executable: `chmod +x scripts/run-evolve-cron.sh`.

3. **Add a crontab entry** (every 4 hours):
   ```bash
   crontab -e
   ```
   Add:
   ```cron
   0 */4 * * * /Users/you/Documents/1_CODE_PROJECTS/llm-orchestrated-systems-design/scripts/run-evolve-cron.sh
   ```
   Use your real path and ensure the script is executable.

Your Mac must be on and Ollama running (or start Ollama in the wrapper) for the agent to run.

### 6. Cursor CLI (headless) — use Cursor’s agent on a schedule (no Anthropic key)

Run the evolution every 4 hours using **Cursor’s built-in agent** from the CLI. Uses your Cursor subscription; no separate Anthropic API key.

1. **Install Cursor CLI** (you said you already did):
   ```bash
   curl https://cursor.com/install -fsS | bash
   ```
   Authenticate so `agent` works. Put `CURSOR_API_KEY=...` in the repo’s `.env`; both scripts load it automatically. To **push after each run**, add to `.env`: `GH_TOKEN=ghp_...` and `REPO=youruser/llm-orchestrated-systems-design`. See [Cursor CLI headless docs](https://cursor.com/docs/cli/headless).

2. **Run one evolution manually:**
   ```bash
   ./scripts/run-evolve-cursor.sh
   ```
   This runs `agent -p --force` with a prompt that mirrors the Python agent: read identity/journal/learnings/takeaways, make one improvement, commit.

3. **Schedule every 4 hours with cron:**
   ```bash
   chmod +x scripts/run-evolve-cursor.sh scripts/run-evolve-cron.sh
   ./scripts/install-cron.sh
   ```
   That installs the cron entry and creates `logs/evolve.log`. Or add by hand: `crontab -e` and add:
   `0 */4 * * * /full/path/to/llm-orchestrated-systems-design/scripts/run-evolve-cron.sh`

4. **Verify the cron job:**
   ```bash
   crontab -l                    # list your cron entries
   ./scripts/run-evolve-cron.sh   # run once (same as cron would)
   tail -50 logs/evolve.log       # check output
   ```
   If `agent` isn’t found when run from cron, ensure Cursor CLI is on your PATH or add its bin path in `run-evolve-cron.sh` (see `PATH=` at the top of the script).

**Antigravity IDE**

[Antigravity IDE](https://antigravityaiide.com/) is Google’s agent-first IDE (Gemini, etc.). Use it interactively for the same “one improvement + journal + commit” workflow. For scheduled runs, use Cursor CLI (above) or the Python agent with Ollama/Anthropic.

---

## How This Looks When Applying for Jobs

### On Your Resume / Portfolio

| Section | What to write |
|---------|----------------|
| **Project name** | "Agentic Design Lab" |
| **One-liner** | "Self-evolving AI agent that iterates on aerospace conceptual designs every 4 hours via GitHub Actions" |
| **Tech** | LLM agents (LangGraph), GitHub Actions, Python, CI/CD, autonomous systems |
| **Highlights** | Scheduled evolution loop, verification gates, journal/learnings memory |

### README Snippets (for your repo)

**Headline:**
```markdown
# Agentic Design Lab

An autonomous agent that evolves spacecraft designs in scheduled cycles.
Runs every 4 hours, reads its own state, plans improvements, and commits.
```

**Architecture diagram:**
```markdown
## Architecture

┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│ GitHub Actions  │────▶│ evolve.sh     │────▶│ LangGraph agent  │
│ (cron: every 4h)│     │ + identity   │     │ reads/writes    │
└─────────────────┘     └──────────────┘     │ designs/, etc.  │
                                             └────────┬────────┘
                                                      │
                                                      ▼
                                             ┌─────────────────┐
                                             │ designs/        │
                                             │ JOURNAL.md      │
                                             │ LEARNINGS.md    │
                                             └─────────────────┘
```

### What People See

- **Automation & DevOps**: Scheduled pipelines, CI/CD, infrastructure-as-code
- **AI / ML**: LLM agent loop, prompt design, autonomous decision-making
- **Systems thinking**: Verification gates, rollback, memory (journal/learnings)
- **Hard tech**: Domain-specific design iteration

### Interview Talking Points

1. **"How does it work?"** — Agent runs on schedule, reads design state and journal, plans one improvement, implements it, commits. Uses verification so bad changes get reverted.
2. **"What did you learn?"** — Balancing autonomy with safety (protected files, human approval for physical build), designing for failure (rollback, retries).
3. **"Why?"** — Combines AI agents with a concrete, multidisciplinary domain (propulsion, structures, regulations).

---

## Checklist Before First Push

- [ ] `ANTHROPIC_API_KEY` in GitHub Secrets
- [ ] `docs/IDENTITY.md` written (or placeholder)
- [ ] `designs/` directory exists
- [ ] Workflow runs (check Actions tab)
