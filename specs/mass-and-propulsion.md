# Mass Budget & Propulsion Requirements — Suborbital Spaceplane (Concept V1)

**Status:** First-pass conceptual estimates for design closure and trajectory studies.  
**Scope:** Suborbital mission per `specs/mission-profile.md` and `designs/concept-v1.md` — not for detailed sizing or certification.

---

## 1. Reference mission and assumptions

- **Mission:** Single-site suborbital hop to 80–100 km apogee, crew or small payload.
- **Reference apogee:** ~100 km (aligned with first trajectory run target).
- **Ascent segments:**
  - Segment A: Air-breathing takeoff + climb to ~25 km, ~Mach 4–6.
  - Segment B: Rocket sustainer from handover to apogee.
- **Descent:** Unpowered glide and landing.

Unless otherwise stated, numbers below are **order-of-magnitude targets** for early trades and are expected to move by ±30–50% as fidelity increases.

---

## 2. Top-level mass budget (conceptual)

Let \(m_0\) be gross liftoff mass (GLOW).

| Mass group                     | Symbol | Target fraction of \(m_0\) | Notes |
|--------------------------------|--------|-----------------------------|-------|
| **Propellant — air-breathing** | \(m_{\text{prop,AB}}\) | 8–12% | Liquid fuel / kerosene-equivalent for takeoff + climb. |
| **Propellant — rocket**        | \(m_{\text{prop,R}}\)  | 18–25% | Oxidizer + fuel for sustainer burn to ~100 km. |
| **Structural & landing gear**  | \(m_{\text{struct}}\)  | 25–32% | Primary structure, TPS allowance, landing gear. |
| **Propulsion hardware**        | \(m_{\text{prop,hw}}\) | 8–12%  | Engines, inlets, nozzles, tanks, feed systems. |
| **Avionics & systems**         | \(m_{\text{sys}}\)     | 4–7%   | GNC, power, ECS (if crewed), hydraulics/actuators. |
| **Payload / crew cabin**       | \(m_{\text{payload}}\) | 3–6%   | Crew, seats, payload, payload bay structure. |
| **Operational margins**        | \(m_{\text{margin}}\)  | 5–8%   | Mass growth allowance and uncertainty. |

Indicative **target range for propellant mass fraction**:

- **Total propellant fraction:** \(m_{\text{prop,AB}} + m_{\text{prop,R}} \approx 26–37\%\ m_0\).
- Early design target: **≈ 30–35%** of \(m_0\) to retain margin for structure and systems.

These fractions should be revisited after:

- Updating trajectory model with better drag/aero and detailed G-limits.
- Introducing simple structural and TPS mass models.

---

## 3. Rocket sustainer requirements (Segment B)

This segment targets the climb from **handover** (~25–30 km, Mach 4–6) to **apogee** (~100 km).

### 3.1 Performance and Δv target

For a first-pass, we adopt a **required effective Δv** band (including gravity and drag losses) rather than a precise trajectory-derived number:

| Quantity                    | Symbol | Target range | Notes |
|----------------------------|--------|--------------|-------|
| Effective Δv (handover → apogee) | \(\Delta v_{\text{eff}}\) | 1.0–1.5 km/s | Coarse band consistent with initial 1-D trajectory runs. |
| Burn time                  | \(t_{\text{burn}}\) | 40–80 s | Tuned vs. G-limits and structural loads. |

These numbers are consistent with the **Day 365 trajectory run** that achieved ~99 km apogee with a short rocket burn and max G < 4 g.

### 3.2 Thrust and thrust-to-weight

Define:

- \(m_{\text{burn}}\): vehicle mass during rocket burn (approx. 0.7–0.9 of \(m_0\)).
- \(T_{\text{vac}}\): vacuum thrust of rocket sustainer.

Design target band:

| Parameter                  | Target band | Rationale |
|---------------------------|-------------|-----------|
| **Initial T/W (Segment B)** | 0.7–1.1 (vacuum equivalent) | Allows modest climb under partial lift; avoids excessive G. |
| **Thrust level**          | 0.7–1.1 × \(m_{\text{burn}} g\) | Tune per trajectory to keep ascent G ≤ 4 g sustained. |

For conceptual closure, one can start with:

- \(T_{\text{vac}} \approx 0.9\,m_{\text{burn}} g\) and adjust with the trajectory solver.

### 3.3 Specific impulse and propellant

| Quantity             | Target | Notes |
|---------------------|--------|-------|
| **Isp (vacuum)**    | 320–350 s | LOX–kerosene or LOX–methane class; un-optimized. |
| **Mixture ratio (O/F)** | 2.5–3.5 | Representative of typical LOX–hydrocarbon engines. |

Required **propellant mass** for a given Δv band can be approximated via the rocket equation for sensitivity studies:

\[
 m_{\text{prop,R}} \approx m_{0,\text{seg}} \left( 1 - e^{-\Delta v_{\text{eff}} / (I_{\text{sp}} g_0)} \right)
\]

where \(m_{0,\text{seg}}\) is the mass at the start of Segment B and \(g_0\) is standard gravity.

For \(\Delta v_{\text{eff}} = 1.2\ \text{km/s}\), \(I_{\text{sp}} = 330\ \text{s}\), and \(m_{0,\text{seg}} \approx 0.8\,m_0\), this yields a **segment propellant fraction** on the order of **10–15% of \(m_0\)**, consistent with the table in §2.

---

## 4. Air-breathing segment requirements (Segment A)

This segment covers **takeoff and climb** to ~25–30 km, Mach 4–6. At this stage we define envelope-level targets rather than a specific cycle.

### 4.1 Thrust and climb capability

High-level thrust and mass flow targets:

| Parameter           | Target band | Notes |
|--------------------|-------------|-------|
| **Sea-level T/W**  | 0.4–0.7     | Allows runway takeoff with lift from wings; avoids fighter-jet-level G. |
| **High-altitude T/W (25–30 km)** | 0.2–0.4 | Sufficient to continue climb/accel with aerodynamic lift. |

These numbers imply **multiple air-breathing units** or a variable-cycle system; the exact configuration is left to future propulsion trades.

### 4.2 Specific fuel consumption & fuel fraction

Expressed as overall **fuel fraction for Segment A**:

| Quantity                           | Target | Notes |
|------------------------------------|--------|-------|
| **Fuel mass fraction (Segment A)** | 8–12% of \(m_0\) | Inclusive of takeoff, climb, and reserves. |
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
  - `designs/concept-v1.md` §3 (“Assumptions and gaps”) should treat these as working targets.
  - Future revisions may split mass groups more finely (e.g., TPS vs. primary structure).

---

## 6. Verification (future)

The following checks should gate future design iterations:

1. **Mass closure:** Sum of all mass fractions in §2 ≤ 1.0, with at least 5–8% reserved as \(m_{\text{margin}}\).  
2. **Trajectory feasibility:** For any selected point in the mass/thrust/Isp bands, trajectory simulations should be able to:
   - Reach 80–100 km apogee, and  
   - Respect G-limits from `specs/mission-profile.md`.  
3. **Sensitivity:** Future studies should quantify sensitivity of apogee and G-loads to ±10–20% changes in:
   - Rocket propellant fraction,  
   - Rocket Isp,  
   - Air-breathing fuel fraction.

---

*First-pass mass and propulsion spec for Concept V1. Human approval required before using these numbers for any physical hardware or regulatory engagement.*

