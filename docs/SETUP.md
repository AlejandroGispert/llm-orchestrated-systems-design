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

### 3. GitHub Secrets

In repo **Settings → Secrets and variables → Actions**, add:

| Secret | Required | Purpose |
|--------|----------|---------|
| `ANTHROPIC_API_KEY` | Yes | LLM API for the agent |
| `GITHUB_TOKEN` | Auto | Push and issues (provided by Actions) |

### 4. Manual Run (local)

```bash
ANTHROPIC_API_KEY=sk-... ./scripts/evolve.sh
```

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
