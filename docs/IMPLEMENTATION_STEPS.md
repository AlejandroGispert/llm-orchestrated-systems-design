# Implementation Steps: Agentic Design Lab

## Research Focus (Concept Domain)

**Target concept class:** Reusable orbital access systems — people from Earth ground → space (smoothly) → return safely to the **same launch spot**.

**Not a rocket** — explore alternative propulsion: spaceplane, air-breathing engines, hybrid systems, or novel concepts.

**Positioning:** Research platform for AI-assisted conceptual design. We are *exploring* how agentic workflows can assist early-stage multidisciplinary design — not building a real crewed vehicle (that is trillion-dollar industrial scale).

---

## Phase 0: Get the Agent Running (Now)

| Step | Action | Verify |
|------|--------|--------|
| 0.1 | `./scripts/setup-venv.sh` (creates `.venv`, installs deps — use on macOS when pip gives "externally-managed-environment") | `python3 -c "from agent.evolve import create_graph; print('ok')"` or `source .venv/bin/activate` then `python -c "from agent.evolve import create_graph; print('ok')"` |
| 0.2 | Add `ANTHROPIC_API_KEY` to GitHub repo Secrets | Settings → Secrets → Actions |
| 0.3 | Ensure `docs/IDENTITY.md`, `docs/JOURNAL.md`, `docs/LEARNINGS.md` exist | `ls -la docs/IDENTITY.md docs/JOURNAL.md docs/LEARNINGS.md` |
| 0.4 | Run locally: `ANTHROPIC_API_KEY=sk-... ./scripts/evolve.sh` | Agent commits one cycle |
| 0.5 | Push to GitHub; trigger workflow manually | Actions tab → Run workflow |

---

## Phase 1: Foundation (Agent Self-Bootstraps)

| Step | Action | Output |
|------|--------|--------|
| 1.1 | Agent creates `designs/concept-v1.md` | First crewed non-rocket concept |
| 1.2 | Agent creates `specs/mission-requirements.md` | Crew count, payload, orbit/suborbital, return-to-launch-site |
| 1.3 | Agent creates `specs/safety-margins.md` | G-limits, abort, redundancy |
| 1.4 | Agent populates `LEARNINGS.md` with design trade-offs | Memory of choices |

---

## Phase 2: Simulation Capability

| Step | Action | Output |
|------|--------|--------|
| 2.1 | Create `simulations/trajectory/` | Trajectory sim (Python: ascent, coast, reentry, landing) |
| 2.2 | Define verification gates in `specs/verification-gates.md` | Pass/fail criteria for sims |
| 2.3 | Agent runs trajectory sim, checks G-loads, landing accuracy | First closed-loop design→simulate→iterate |
| 2.4 | Add structural model (simplified FEA or analytical) | Loads, margins |
| 2.5 | Add thermal model (reentry heating) | TPS sizing, limits |

---

## Phase 3: Subsystem Design

| Step | Action | Output |
|------|--------|--------|
| 3.1 | Propulsion: engine choice, thrust, Isp, fuel/oxidizer, tanks | `designs/propulsion-v1.md` |
| 3.2 | Structures: airframe, materials, loads, mass budget | `designs/structures-v1.md` |
| 3.3 | Thermal: reentry profile, TPS/ablative, cooling | `designs/thermal-v1.md` |
| 3.4 | Avionics: GNC, sensors, flight computer, power | `designs/avionics-v1.md` |
| 3.5 | Life support: pressure, O2, CO2, redundancy for crew | `designs/life-support-v1.md` |
| 3.6 | Trade studies document rationale | `designs/trade-studies.md` |

---

## Phase 4: Integration & Compliance

| Step | Action | Output |
|------|--------|--------|
| 4.1 | Full vehicle concept: layout, masses, interfaces | `designs/vehicle-integrated-v1.md` |
| 4.2 | Compliance matrix vs FAA Part 450, Part 460 | `specs/compliance-matrix.md` |
| 4.3 | Test plan: component, subsystem, integration, flight | `specs/test-plan.md` |
| 4.4 | Human review checkpoints | Agent flags for expert sign-off |

---

## Phase 5: Build Support (Human-Led)

| Step | Action | Output |
|------|--------|--------|
| 5.1 | Manufacturing specs, drawings, procedures | Agent drafts; human approves |
| 5.2 | QA plans, NDT, acceptance criteria | Agent drafts |
| 5.3 | Flight test plan, range coordination | Agent drafts |
| 5.4 | Human executes build, test, licensing | Agent supports docs only |

---

## Tools to Add (Future)

| Tool | Purpose |
|------|---------|
| `run_simulation` | Execute trajectory/structural/thermal sims |
| `web_search` | Look up standards, papers, regulations |
| `curl` / HTTP | Fetch NASA docs, FAA rules, specs |
| `plot` | Generate charts for trade studies |

---

## Quick Start Checklist

- [ ] `./scripts/setup-venv.sh` (or `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`)
- [ ] `ANTHROPIC_API_KEY` in GitHub Secrets
- [ ] `docs/IDENTITY.md` defines research focus: conceptual design of reusable orbital access (ground→space→same-spot return)
- [ ] Run `./scripts/evolve.sh` locally once
- [ ] Push; confirm Actions run
- [ ] Let agent create first design in `designs/`
