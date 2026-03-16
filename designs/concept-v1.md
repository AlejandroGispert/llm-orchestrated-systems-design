# Concept V1 — First Conceptual Design

**Status:** Conceptual only. No fabrication. Research platform artifact.  
**Mission alignment:** Reusable orbital access — ground → space → return to same launch spot; not a rocket; explore alternatives.

---

## 1. Concept summary

**Working name:** Suborbital spaceplane (air-breathing + rocket sustainer).

- **Outbound:** Horizontal takeoff from same pad; air-breathing propulsion to high altitude/speed; rocket sustainer for final push to suborbital apogee.
- **Return:** Re-entry, glide, same-site landing (runway or designated pad).
- **Rationale for “not a rocket”:** Reduces pure-vertical rocket stack; explores air-breathing for part of the trajectory; same-site return constrains operations and enables repeated use of one location.

---

## 2. High-level architecture (conceptual)

| Element | Concept |
|--------|--------|
| **Propulsion (ascent)** | Air-breathing (e.g. turbojet/ramjet) for low-to-mid altitude; liquid rocket sustainer for exoatmospheric leg. |
| **Propulsion (descent)** | Unpowered glide; possibly small thrust for go-around or abort. |
| **Structure** | Lifting body or winged vehicle; materials TBD (conceptual stage). |
| **Landing** | Wheeled runway or vertical landing on pad — to be traded. |
| **Crew/cargo** | Suborbital: small crew or payload; orbital variant deferred. |

---

## 3. Assumptions and gaps

- **Assumptions:** Single launch/landing site; suborbital first; regulatory framework (e.g. FAA Part 450/460) applies when moving toward implementation. Nominal flights are expected to meet **trajectory requirements TR-1/2** as defined in `specs/trajectory-requirements.md`:
  - **TR-1 (Apogee band):** Apogee within 80–100 km for nominal flights as computed by `simulations/trajectory_v1.py` (or successors), with design knobs (T/W, Δv, mass fractions) chosen so the achieved apogee sits near the middle of the band with margin in both directions.
  - **TR-2 (Ascent G-band):** Ascent G-loads within the bands implied by `specs/mission-profile.md` and checked in trajectory runs (sustained ≤4 g, brief peaks ≤5 g), consistent with a “slow ascent / slow descent” philosophy captured in `docs/LEARNINGS.md`.
- **Gaps:** Current trajectory model is 1-D and coarse; mass budget and propulsion bands are first-pass only; no structural/thermal sizing; no detailed propulsion cycle or fuel choice fixed. The “slow ascent / slow descent” and low‑q climb concepts are not yet enforced via explicit **TR-3/4** dynamic-pressure and re-entry corridor gates, nor are they backed by aero/thermal models. These gaps are intended to be closed by:
  - Extending trajectory simulations to compute dynamic pressure vs. altitude and speed so candidate TR-3/4 limits can be defined and verified.
  - Iterating `specs/mass-and-propulsion.md` so that the chosen T/W, Δv, and propellant-fraction bands remain compatible with any future dynamic-pressure and re-entry constraints derived from aero/thermal studies.

---

## 4. Next steps (for future sessions)

1. Refine and re-run trajectory simulations using `specs/mission-profile.md`, `specs/mass-and-propulsion.md`, and `specs/trajectory-requirements.md` as explicit inputs and gates — i.e., design knobs (T/W, Δv, mass fractions) are adjusted until **TR-1/2** are satisfied with margin.
2. Iterate the mass budget and propulsion bands in `specs/mass-and-propulsion.md` based on trajectory sensitivity (e.g., apogee and G-load response to ±10–20% changes in propellant fractions and Isp) while keeping TR-1/2 satisfied.
3. Introduce first-pass aero/structural assumptions (L/D targets, structural mass splits, TPS allowance) consistent with the “slow ascent / slow descent” concept and draft **TR-3/4** dynamic-pressure and re-entry limits.
4. Refine or replace this concept based on coupled trajectory–mass–aero trade studies and any new trajectory requirement IDs that emerge from higher-fidelity models.

---

*First conceptual design document. Created by the aerospace conceptual design agent. Human approval required before any physical build step.*
