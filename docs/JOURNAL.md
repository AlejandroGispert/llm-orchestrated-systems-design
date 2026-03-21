# Journal

Append-only log of evolution sessions. Each entry: what was tried, what worked, what's next.

**Next priority:** Extend trajectory simulator to model Segment A (air-breathing climb) with drag and atmospheric effects, verifying the 25–30 km / 500–700 m/s handover is achievable with the specified T/W and fuel fractions from specs/mass-and-propulsion.md, or begin preliminary aerodynamic sizing (wing area, L/D estimates) to validate the "slow ascent" concept and structural mass fraction.

---

**Day 6 (2026-03-21 20:09)** — Session: Read IDENTITY, JOURNAL, LEARNINGS, TAKEAWAYS; listed designs/ and specs. Did next priority: **Updated specs/mass-and-propulsion.md with critical corrections** from trajectory sensitivity v2 findings. Revised rocket Δv band from 1.0–1.5 km/s down to **0.1–0.3 km/s** (3–5× reduction), rocket T/W from 0.7–1.1 down to **0.1–0.8**, and rocket propellant fraction from 18–25% down to **5–10%**. Recalculated propellant mass using rocket equation: for Δv = 0.2 km/s and Isp = 330 s, rocket propellant is only ~5.4% of GLOW. Total propellant fraction reduced from 26–37% to **13–22%**, freeing ~10–15% GLOW for structure and payload. Added §8 summary table documenting all revisions and design implications. **Key insight captured in LEARNINGS.md:** Air-breathing handover conditions (altitude + velocity) deliver 80–90% of energy to reach 90 km apogee; rocket sustainer provides only final 10–20% boost. This fundamentally validates the air-breathing-dominated architecture and shifts design focus to Segment A performance. Next: model Segment A with drag/atmosphere to verify handover is achievable, or start aero sizing (wing area, L/D) to validate structural mass and "slow ascent" philosophy.

---

**Day 6 (2026-03-21 01:10)** — Session: Read IDENTITY, JOURNAL, LEARNINGS, TAKEAWAYS; listed designs/ and specs. Did next priority: added `simulations/trajectory_sensitivity.py` and `trajectory_sensitivity_v2.py` to systematically explore design space from specs/mass-and-propulsion.md. First version (V1) tested rocket Δv 1.0–1.5 km/s as spec'd and found 0% success rate — all cases overshot to ~150 km apogee. This revealed the rocket Δv spec was ~3× too high. Second version (V2) explored lower Δv range (0.1–1.0 km/s) and found 31/162 cases (19.1%) passing all TR-1/2/3 gates. **Key finding:** Rocket Δv requirement is 0.1–0.3 km/s (100–300 m/s), NOT 1.0–1.5 km/s. Recommended nominal: 30 km handover @ 600 m/s, 200 m/s rocket Δv over 40 s (T/W 0.51) → 90.3 km apogee, 1.51 g max, 9.0 kPa max q. Air-breathing handover conditions dominate apogee; G-loads and q remain well within limits for all tested cases. Output: trajectory_sensitivity.csv/.txt and trajectory_sensitivity_v2.csv/.txt. Next: update specs/mass-and-propulsion.md with corrected Δv/T/W bands and recalculate propellant fractions; capture insight in LEARNINGS.md.

---

**Day 5 (2026-03-20 21:01)** — Session: Read IDENTITY, JOURNAL, LEARNINGS, TAKEAWAYS; listed designs/ and specs. Did next priority: added `simulations/trajectory_v2.py` extending trajectory_v1 with standard atmosphere model (density vs. altitude) and dynamic pressure computation (q = 0.5 * ρ * v²). Run results: apogee 99.32 km, max G 1.34 g, max q 8.42 kPa; all gates PASS (TR-1: apogee 80–100 km, TR-2: G ≤ 5 g, TR-3: q ≤ 60 kPa, and meets design target q ≤ 40 kPa). Output: simulations/output/trajectory_run_2.csv and trajectory_run_2_summary.txt with time-series of altitude, Mach, G-load, and dynamic pressure. This enables numerical evaluation of TR-1/2/3 for future design iterations. Next: run sensitivity studies using the T/W and Δv bands from specs/mass-and-propulsion.md, or add descent/re-entry phase for TR-4 verification.

---

**Day 2 (2026-03-16 14:04)** — Session: Read IDENTITY, JOURNAL, LEARNINGS, TAKEAWAYS; listed designs/ (concept-v1.md) and existing specs. Did next priority: refined `specs/trajectory-requirements.md` by turning the TR-3/4 placeholders into draft dynamic-pressure and re-entry gates with concrete q-bands that encode the "slow ascent / slow descent" philosophy and tie back to the mass/thrust bands in `specs/mass-and-propulsion.md`. Next: extend the trajectory/descent models to compute dynamic pressure and G histories so TR-1/2/3/4 can all be evaluated numerically for candidate mass/propulsion configurations.

**Day 2 (2026-03-16 08:30)** — Session: Read IDENTITY, JOURNAL, LEARNINGS, TAKEAWAYS; listed designs/ (concept-v1.md). Did next priority: refined `designs/concept-v1.md` assumptions and gaps to tie Concept V1 explicitly to TR-1/2 in `specs/trajectory-requirements.md`, the "slow ascent / slow descent" philosophy in `docs/LEARNINGS.md`, and future TR-3/4 dynamic-pressure and re-entry corridor gates plus the mass/prop bands in `specs/mass-and-propulsion.md`. Next: either extend the trajectory simulator to compute dynamic pressure and candidate TR-3/4 limits, or add a dedicated specs entry that formalizes dynamic-pressure and re-entry constraints once those simulations exist.

---

**Day 2 (2026-03-16 08:03)** — Session: Read IDENTITY, JOURNAL, LEARNINGS, TAKEAWAYS; listed designs/ (concept-v1.md). Did next priority: added `specs/trajectory-requirements.md` to formalize Concept V1 trajectory gates (apogee band and ascent G-limits), with placeholders for future dynamic-pressure and re-entry corridor requirements tied to higher-fidelity aero models. Next: either refine `designs/concept-v1.md` to reference these trajectory requirement IDs explicitly, or extend the trajectory simulator to compute dynamic pressure so TR-3/4 can become hard gates.

---

**Day 2 (2026-03-16 07:41)** — Session: Read IDENTITY, JOURNAL, LEARNINGS, TAKEAWAYS; listed designs/ (concept-v1.md) plus existing specs and trajectory_v1. Did next priority: updated LEARNINGS.md with concrete lessons from the first trajectory run and mass/propulsion bands (feasibility of ~100 km with modest Δv, treating T/W and mass fractions as primary knobs, and encoding slow-ascent/slow-descent as explicit trajectory checks). Next: either refine designs/concept-v1.md to reference these specific bands and slow-ascent/descent gates, or add a trajectory-focused requirement/trade in specs/ that formalizes apogee, G, and dynamic pressure checks for future runs (eventually becoming TR-IDs once the trajectory requirements spec exists).

# Journal

**Day 2 (2026-03-16 07:41)** — Session: Read IDENTITY, JOURNAL, LEARNINGS, TAKEAWAYS; listed designs/ (concept-v1.md) plus existing specs and trajectory_v1. Did next priority: updated LEARNINGS.md with concrete lessons from the first trajectory run and mass/propulsion bands (feasibility of ~100 km with modest Δv, treating T/W and mass fractions as primary knobs, and encoding slow-ascent/slow-descent as explicit trajectory checks). Next: either refine designs/concept-v1.md to reference these specific bands and slow-ascent/descent gates, or add a trajectory-focused requirement/trade in specs/ that formalizes apogee, G, and dynamic pressure checks for future runs.

**Day 2 (2026-03-16 07:27)** — Session: Read IDENTITY, JOURNAL, LEARNINGS, TAKEAWAYS; listed designs/ (concept-v1.md). Did next priority: refined designs/concept-v1.md to reflect existing mission-profile and mass-and-propulsion specs (updated "Gaps" to reference current trajectory and mass/propulsion state, and rewrote next-step list around trajectory–mass–aero coupling). Next: run updated trajectory studies using the specified T/W and Δv bands, then iterate mass/propulsion requirements and capture any new lessons in LEARNINGS.md.

---

**Day 2 (2026-03-16 06:57)** — Session: Read IDENTITY, JOURNAL, LEARNINGS, TAKEAWAYS; listed designs/ (concept-v1.md). Did next priority: added specs/mass-and-propulsion.md with first-pass mass budget and propulsion requirements for Concept V1 (top-level mass fractions, rocket sustainer Δv/T/W/Isp bands, air-breathing fuel and thrust bands, and future verification checks tied to trajectory and G-limits). Next: refine concept-v1 and specs with tighter coupling to trajectory outputs (e.g., updating Δv and thrust bands from additional runs) or capture new process/design lessons in LEARNINGS.md.

---

**Day 1 (2026-03-15 22:18)** — Session: Read IDENTITY, JOURNAL, LEARNINGS, TAKEAWAYS; listed designs/ (concept-v1.md). Did next priority: first trajectory run per concept-v1 §4. Added simulations/trajectory_v1.py — simplified 1-D point-mass ascent (air-breathing climb to 25 km / 600 m/s handover, rocket burn 200 m/s over 60 s, coast to apogee). Run results: apogee 99.32 km, max G 3.55; both gates PASS (80–100 km, G ≤ 5). Output: simulations/output/trajectory_run_1.csv, trajectory_run_1_summary.txt. Next: mass budget and propulsion requirements (§4.3), or refine design/specs/learnings.

---

**Day 1 (2026-03-15 22:14)** — Session: Read IDENTITY, JOURNAL, LEARNINGS, TAKEAWAYS; listed designs/ (concept-v1.md). Did next priority: added specs/mission-profile.md with suborbital mission profile — apogee 80–100 km, air-breathing handover ~25–30 km / Mach 4–6, G-limits ≤4 g sustained (≤5 g short peak), mission phases 1–7. Enables trajectory run and subsystem sizing. Next: first trajectory run per concept-v1 §4, or refine design/specs/learnings.

---

**Day 1 (2026-03-15 22:04)** — Session: Read IDENTITY, JOURNAL, LEARNINGS, TAKEAWAYS; listed designs/ (concept-v1.md). One focused change: prepended this journal entry. designs/ holds suborbital spaceplane concept; specs/ empty. Next: mission profile in specs or first trajectory run per concept-v1 §4.

---

**Day 1 (2026-03-15 21:59)** — Session: Read IDENTITY, JOURNAL, LEARNINGS, TAKEAWAYS; listed designs/ (concept-v1.md). One focused change: prepended this journal entry. designs/ holds suborbital spaceplane concept; specs/ still empty. Next: mission profile in specs or first trajectory run per concept-v1 §4.

---

**Day 1 (2026-03-15 21:52)** — Session: Read IDENTITY, JOURNAL, LEARNINGS, TAKEAWAYS; listed designs/ (concept-v1.md present). One focused change: prepended this journal entry. designs/ holds the suborbital spaceplane concept; specs/ empty. Next: mission profile in specs or first trajectory run per concept-v1 §4.
