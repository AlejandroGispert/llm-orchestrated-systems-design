# Mass Budget & Propulsion Requirements — Suborbital Spaceplane (Concept V1)

**Status:** Second revision (Day 6) — updated rocket Δv/T/W bands from trajectory sensitivity studies.  
**Scope:** Suborbital mission per `specs/mission-profile.md` and `designs/concept-v1.md` — not for detailed sizing or certification.

---

## 1. Reference mission and assumptions

- **Mission:** Single-site suborbital hop to 80–100 km apogee, crew or small payload.
- **Reference apogee:** ~90 km (aligned with trajectory sensitivity v2 recommended nominal).
- **Ascent segments:**
  - Segment A: Air-breathing takeoff + climb to ~25–30 km, ~Mach 4–6 (500–700 m/s).
  - Segment B: Rocket sustainer from handover to apogee.
- **Descent:** Unpowered glide and landing.

Unless otherwise stated, numbers below are **order-of-magnitude targets** for early trades and are expected to move by ±30–50% as fidelity increases.

---

## 2. Top-level mass budget (conceptual)

Let \(m_0\) be gross liftoff mass (GLOW).

| Mass group                     | Symbol | Target fraction of \(m_0\) | Notes |
|--------------------------------|--------|-----------------------------|-------|
| **Propellant — air-breathing** | \(m_{\text{prop,AB}}\) | 8–12% | Liquid fuel / kerosene-equivalent for takeoff + climb. |
| **Propellant — rocket**        | \(m_{\text{prop,R}}\)  | 5–10% | **Revised down** from 18–25%; oxidizer + fuel for sustainer burn. |
| **Structural & landing gear**  | \(m_{\text{struct}}\)  | 30–37% | **Revised up** to accommodate reduced propellant fraction; primary structure, TPS, landing gear. |
| **Propulsion hardware**        | \(m_{\text{prop,hw}}\) | 8–12%  | Engines, inlets, nozzles, tanks, feed systems. |
| **Avionics & systems**         | \(m_{\text{sys}}\)     | 4–7%   | GNC, power, ECS (if crewed), hydraulics/actuators. |
| **Payload / crew cabin**       | \(m_{\text{payload}}\) | 3–6%   | Crew, seats, payload, payload bay structure. |
| **Operational margins**        | \(m_{\text{margin}}\)  | 5–8%   | Mass growth allowance and uncertainty. |

**Revised total propellant fraction:**

- **Total propellant fraction:** \(m_{\text{prop,AB}} + m_{\text{prop,R}} \approx 13–22\%\ m_0\) (**down from 26–37%**).
- Early design target: **≈ 15–20%** of \(m_0\), freeing up margin for structure, systems, and payload.

**Rationale for revision:** Trajectory sensitivity v2 (Day 6) demonstrated that rocket Δv requirements are 0.1–0.3 km/s, not 1.0–1.5 km/s. This dramatically reduces propellant mass and shifts the design toward a higher-structure, lower-propellant architecture.

These fractions should be revisited after:

- Updating trajectory model with drag model for Segment A.
- Introducing simple structural and TPS mass models.
- Conducting descent trajectory studies to refine glide requirements.

---

## 3. Rocket sustainer requirements (Segment B)

This segment targets the climb from **handover** (~25–30 km, Mach 4–6 / 500–700 m/s) to **apogee** (~90 km).

### 3.1 Performance and Δv target — **REVISED**

Updated based on trajectory sensitivity v2 (Day 6, simulations/output/trajectory_sensitivity_v2_summary.txt):

| Quantity                    | Symbol | Target range | Notes |
|----------------------------|--------|--------------|-------|
| **Effective Δv (handover → apogee)** | \(\Delta v_{\text{eff}}\) | **0.1–0.3 km/s** | **Revised down** from 1.0–1.5 km/s. Sufficient for 80–100 km apogee when handover is at 25–30 km and 500–700 m/s. |
| **Burn time**                  | \(t_{\text{burn}}\) | 40–80 s | Tuned vs. G-limits and structural loads. |
| **Recommended nominal**        | — | 0.2 km/s over 40 s | From sensitivity v2 best case: 30 km handover, 600 m/s, → 90.3 km apogee, 1.51 g max. |

**Key finding (Day 6):** The air-breathing segment delivers the vehicle to 25–30 km with 500–700 m/s of horizontal velocity. At this point, the vehicle already has substantial kinetic and potential energy. The rocket sustainer only needs to add 100–300 m/s of Δv to coast to ~90 km apogee. The original 1.0–1.5 km/s estimate was **3–5× too high** and would overshoot to 150+ km.

### 3.2 Thrust and thrust-to-weight — **REVISED**

Define:

- \(m_{\text{burn}}\): vehicle mass during rocket burn (approx. 0.85–0.95 of \(m_0\), since air-breathing fuel is already consumed).
- \(T_{\text{vac}}\): vacuum thrust of rocket sustainer.

**Revised design target band:**

| Parameter                  | Target band | Rationale |
|---------------------------|-------------|-----------|
| **T/W (Segment B, vacuum equivalent)** | **0.1–0.8** | **Revised down** from 0.7–1.1. Lower bound allows gentle climb under partial lift and low G; upper bound avoids excessive G. |
| **Thrust level (recommended nominal)** | **0.5 × \(m_{\text{burn}} g\)** | T/W ≈ 0.51 from sensitivity v2 best case yields 1.51 g max and 90.3 km apogee. |

For conceptual closure:

- Start with \(T_{\text{vac}} \approx 0.5\,m_{\text{burn}} g\) and adjust with the trajectory solver.
- The reduced thrust requirement implies **smaller rocket engines** and **lower structural loads** on the vehicle during powered ascent.

### 3.3 Specific impulse and propellant

| Quantity             | Target | Notes |
|---------------------|--------|-------|
| **Isp (vacuum)**    | 320–350 s | LOX–kerosene or LOX–methane class; un-optimized. |
| **Mixture ratio (O/F)** | 2.5–3.5 | Representative of typical LOX–hydrocarbon engines. |

**Required propellant mass** for a given Δv band via the rocket equation:

\[
 m_{\text{prop,R}} \approx m_{0,\text{seg}} \left( 1 - e^{-\Delta v_{\text{eff}} / (I_{\text{sp}} g_0)} \right)
\]

**Revised calculation (Day 6):**

- Assume \(\Delta v_{\text{eff}} = 0.2\ \text{km/s}\), \(I_{\text{sp}} = 330\ \text{s}\), and \(m_{0,\text{seg}} \approx 0.9\,m_0\) (most air-breathing fuel consumed).
- Rocket propellant fraction:

\[
 \frac{m_{\text{prop,R}}}{m_0} \approx 0.9 \left( 1 - e^{-200 / (330 \times 9.81)} \right) \approx 0.9 \times 0.0601 \approx 0.054 \approx \mathbf{5.4\%}
\]

- For the upper bound (\(\Delta v = 0.3\ \text{km/s}\)):

\[
 \frac{m_{\text{prop,R}}}{m_0} \approx 0.9 \left( 1 - e^{-300 / (330 \times 9.81)} \right) \approx 0.9 \times 0.0885 \approx \mathbf{8.0\%}
\]

**Result:** Rocket propellant fraction of **5–10% of \(m_0\)** is sufficient, consistent with the revised table in §2. This is a **60–70% reduction** from the initial 18–25% estimate.

---

## 4. Air-breathing segment requirements (Segment A)

This segment covers **takeoff and climb** to ~25–30 km, Mach 4–6 (500–700 m/s). At this stage we define envelope-level targets rather than a specific cycle.

### 4.1 Thrust and climb capability

High-level thrust and mass flow targets:

| Parameter           | Target band | Notes |
|--------------------|-------------|-------|
| **Sea-level T/W**  | 0.4–0.7     | Allows runway takeoff with lift from wings; avoids fighter-jet-level G. |
| **High-altitude T/W (25–30 km)** | 0.2–0.4 | Sufficient to continue climb/accel with aerodynamic lift to handover conditions. |

These numbers imply **multiple air-breathing units** or a variable-cycle system; the exact configuration is left to future propulsion trades.

**Note (Day 6):** Trajectory sensitivity v2 confirms that reaching handover conditions (25–30 km, 500–700 m/s) is the **critical design driver** for apogee. The air-breathing segment delivers ~80–90% of the energy required to reach 90 km apogee; the rocket sustainer provides only the final 10–20% boost. This makes Segment A propulsion **the most important subsystem** for mission success.

### 4.2 Specific fuel consumption & fuel fraction

Expressed as overall **fuel fraction for Segment A**:

| Quantity                           | Target | Notes |
|------------------------------------|--------|-------|
| **Fuel mass fraction (Segment A)** | 8–12% of \(m_0\) | Inclusive of takeoff, climb, and reserves. Unchanged from first revision. |
| **SFC (cruise/climb)**            | Order-of-magnitude consistent with advanced turbo/ramjet systems | Detailed cycle left for later. |

The trajectory model should treat this fuel as:

- A mass decrement over time for Segment A,  
- With bounds such that the vehicle still has sufficient mass and energy for Segment B to meet apogee targets.

---

## 5. Constraints and interfaces

These mass and propulsion targets shall be used as **design constraints** and **initial guesses** for simulations:

- **Trajectory solver interface:**
  - Inputs: \(m_0\), mass fractions from §2, thrust and Isp bands from §§3–4.
  - Outputs: Apogee, G-history, dynamic pressure; used to adjust T/W and Δv bands.
- **Design documents:**
  - `designs/concept-v1.md` §3 ("Assumptions and gaps") should treat these as working targets.
  - Future revisions may split mass groups more finely (e.g., TPS vs. primary structure).

---

## 6. Verification (future)

The following checks should gate future design iterations:

1. **Mass closure:** Sum of all mass fractions in §2 ≤ 1.0, with at least 5–8% reserved as \(m_{\text{margin}}\).  
2. **Trajectory feasibility:** For any selected point in the mass/thrust/Isp bands, trajectory simulations should be able to:
   - Reach 80–100 km apogee, and  
   - Respect G-limits from `specs/mission-profile.md`.  
3. **Sensitivity:** Future studies should quantify sensitivity of apogee and G-loads to ±10–20% changes in:
   - **Air-breathing handover conditions** (altitude, velocity) — **now recognized as primary driver**,
   - Rocket propellant fraction,  
   - Rocket Isp.

---

## 7. Slow ascent / slow descent design hooks

To support the **slow, efficient climb** and **gentle descent** concept from `specs/mission-profile.md`:

- **Segment A (slow ascent, drone-like):**
  - Aim for **Sea-level T/W** at the low end of the 0.4–0.7 band when operating in "economy climb" mode.
  - Require the trajectory to demonstrate:
    - Climb to at least 15–20 km with average G-loads ≈1–2 g, and  
    - Dynamic pressure kept below a to-be-defined limit (e.g. q ≤ 20–30 kPa) in this segment.
  - Mass budget should preserve sufficient wing area and structural margin to fly at high L/D and low sink/climb rates.

- **Stratosphere boost (handover prep):**
  - A higher-thrust "boost" sub-mode may temporarily raise effective T/W within the Segment A/B envelope to hit the handover Mach/altitude.
  - When this mode is active, the combination of thrust, mass, and ascent profile shall still respect the 4 g sustained limit.

- **Descent and recovery:**
  - End-of-mission mass and aerodynamic configuration should allow:
    - Long, shallow glide with sink rates and G-loads compatible with crew/payload comfort (≈1–2 g nominal).  
    - Optional use of air-braking or high-drag modes without exceeding structural limits.

These hooks give trajectory and aero/controls studies concrete levers (T/W bands, mass fractions, and L/D expectations) to test whether the "slow ascent / slow descent" idea can be made practical without breaking the mass and performance closure above.

---

## 8. Summary of Day 6 revisions

**Critical corrections based on trajectory sensitivity v2:**

| Parameter | Original (Day 2) | Revised (Day 6) | Change |
|-----------|------------------|-----------------|--------|
| Rocket Δv | 1.0–1.5 km/s | **0.1–0.3 km/s** | **−70 to −80%** |
| Rocket T/W | 0.7–1.1 | **0.1–0.8** | **Lower bound −86%; upper bound −27%** |
| Rocket propellant fraction | 18–25% | **5–10%** | **−60 to −70%** |
| Total propellant fraction | 26–37% | **13–22%** | **−50 to −60%** |
| Structural fraction | 25–32% | **30–37%** | **+16 to +19%** |

**Design implications:**

1. **Smaller rocket engines:** Lower thrust and Δv requirements → lighter propulsion hardware and lower structural loads.
2. **Lower propellant mass:** Frees up ~10–15% of GLOW for structure, payload, and margins.
3. **Air-breathing segment is critical:** Handover conditions (altitude + velocity) determine 80–90% of final apogee; rocket sustainer provides only final boost.
4. **Architecture validation:** The "air-breathing climb + small rocket kick" concept is **feasible and efficient** for 80–100 km suborbital missions.

---

*Second revision of mass and propulsion spec for Concept V1. Human approval required before using these numbers for any physical hardware or regulatory engagement.*
