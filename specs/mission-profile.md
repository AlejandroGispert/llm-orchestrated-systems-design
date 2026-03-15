# Mission Profile — Suborbital Spaceplane (Concept V1)

**Status:** Spec for design/simulation. Aligns with designs/concept-v1.md.  
**Purpose:** Define altitude, Mach, G-limits, and mission phases for trajectory and subsystem sizing.

---

## 1. Mission summary

- **Type:** Suborbital, crew or small payload.
- **Outbound:** Horizontal takeoff → air-breathing climb/accel → rocket sustainer → apogee.
- **Return:** Re-entry → glide → same-site landing (runway or pad).
- **Single site:** Launch and land at same location.

---

## 2. Key parameters

| Parameter | Value | Notes |
|-----------|--------|--------|
| **Apogee (target)** | 80–100 km | Suborbital; 100 km = Kármán line reference. |
| **Air-breathing segment** | Takeoff to ~25–30 km, Mach 4–6 (conceptual) | Ramjet/scramjet regime; exact envelope TBD by propulsion trade. |
| **Sustainer ignition** | ~25–30 km, Mach 4–6 | Handover from air-breathing to rocket. |
| **Max G (ascent)** | ≤ 4 g sustained | Crew comfort / payload limit; peaks ≤ 5 g short duration. |
| **Max G (re-entry/descent)** | ≤ 4 g sustained | Glide and pull-up; avoid excessive heating and load. |
| **Landing** | Runway or designated pad at same site | Speed/energy state TBD by trajectory. |

---

## 3. Mission phases (reference)

1. **Takeoff / roll** — Horizontal acceleration to rotation speed.
2. **Climb (air-breathing)** — Climb and accelerate to sustainer handover altitude/Mach.
3. **Sustainer burn** — Rocket push to apogee (80–100 km).
4. **Coast / apogee** — Brief microgravity; duration TBD.
5. **Re-entry** — Unpowered re-entry; G and heating within limits.
6. **Glide** — Unpowered glide to landing site.
7. **Approach / landing** — Runway or pad; go-around capability TBD.

---

## 4. Constraints for trajectory run

- Altitude: target 80–100 km apogee.
- Mach: air-breathing leg to ~Mach 4–6 at handover; trajectory to close.
- G-limits: 4 g sustained, 5 g short peak (ascent and descent).
- Same-site return: landing within operational envelope of launch site.
- No orbit: suborbital only; no circular orbit insertion.

---

## 5. Verification (future)

- Trajectory simulation shall achieve apogee in 80–100 km band.
- Simulated G-history shall not exceed limits above.
- Heating and dynamic pressure along trajectory to be checked in later thermal/structural passes.

---

*Mission profile for conceptual design and first trajectory runs. Human approval required before physical build or test.*
