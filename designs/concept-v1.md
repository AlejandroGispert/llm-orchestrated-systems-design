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

- **Assumptions:** Single launch/landing site; suborbital first; regulatory framework (e.g. FAA Part 450/460) applies when moving toward implementation.
- **Gaps:** Current trajectory model is 1-D and coarse; mass budget and propulsion bands are first-pass only; no structural/thermal sizing; no detailed propulsion cycle or fuel choice fixed. These are planned for later design iterations and simulation gates tied to the existing mission profile and mass/propulsion specs.

---

## 4. Next steps (for future sessions)

1. Refine and re-run trajectory simulations using `specs/mission-profile.md` and `specs/mass-and-propulsion.md` as explicit inputs (apogee, G-limits, T/W and Δv bands).
2. Iterate the mass budget and propulsion bands based on trajectory sensitivity (e.g., apogee and G-load response to ±10–20% changes in propellant fractions and Isp).
3. Introduce first-pass aero/structural assumptions (L/D targets, structural mass splits, TPS allowance) consistent with the “slow ascent / slow descent” concept.
4. Refine or replace this concept based on coupled trajectory–mass–aero trade studies.

---

*First conceptual design document. Created by the aerospace conceptual design agent. Human approval required before any physical build step.*
