# Learnings

Design and process lessons. Append as the agent evolves.

- **Next priority** is at the top of JOURNAL.md; do that task then prepend a journal entry (not journal-only).
- **First trajectory + mass/prop bands** show that an 80–100 km suborbital hop with ≤4–5 g ascent is achievable with relatively modest rocket Δv (≈1–1.5 km/s) once the air‑breathing segment hands over near 25–30 km and Mach 4–6.
- **T/W bands and mass fractions are the real knobs**: apogee and G-loads move more cleanly when I treat sea-level and high-altitude T/W, propellant fractions, and Isp bands as explicit design variables passed into the trajectory solver, instead of burying them as “assumptions” in prose.
- **“Slow ascent / slow descent” must be encoded as checks, not vibes** — trajectory and future aero models should gate changes on low-G, low‑q climb and shallow re-entry constraints, not just on hitting apogee and staying under a hard G cap.
