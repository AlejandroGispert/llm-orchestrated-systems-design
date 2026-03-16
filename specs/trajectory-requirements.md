## Trajectory Requirements — Concept V1

Derived from `specs/mission-profile.md`, `specs/mass-and-propulsion.md`, and the first trajectory run (`simulations/trajectory_v1.py`).

These are **concept-level gates** for ascent and coast; detailed aero/thermal limits (e.g., max dynamic pressure) will be added once a higher-fidelity model exists.

---

### 1. Ascent and Apogee Requirements

| ID | Requirement | Rationale | Verification (current) |
|----|-------------|-----------|------------------------|
| TR-1 | Suborbital apogee shall lie in the range **80–100 km** for nominal missions. | Matches mission profile target band and demonstrated feasibility in trajectory_run_1 (≈99 km). | Check max altitude from `trajectory_v1` output summary / CSV. |
| TR-2 | Sustained ascent G-load (body-axis) shall be **≤ 4 g**, with short peaks **≤ 5 g** allowed during transitions. | Aligns with mission-profile comfort/safety band and initial run (≈3.5 g peak). | Compute G from acceleration history in `trajectory_v1` and confirm thresholds. |

---

### 2. Aero / Dynamic-Pressure and Re-entry Gates (Draft)

These are **draft requirements** that operationalize the “slow ascent / slow descent” philosophy from `specs/mission-profile.md` and the mass/thrust bands in `specs/mass-and-propulsion.md`. They remain subject to revision as aero/thermal and structural models increase in fidelity, but they give trajectory studies concrete numeric targets to design against.

| ID | Requirement (draft) | Notes |
|----|---------------------|-------|
| TR-3 | Maximum dynamic pressure \( q_\text{max} \) during **ascent** shall not exceed **60 kPa** for nominal missions, with a design target of **≤ 40 kPa** in the “slow climb” portion below ~20 km. | Reflects the intent in `specs/mission-profile.md` and `specs/mass-and-propulsion.md` to keep early climb drone-like and low‑q; exact values to be revisited once coupled aero/structural models exist. Requires extending the trajectory solver with an atmosphere model to compute \( q = \tfrac{1}{2}\rho V^2 \) along the path. |
| TR-4 | The **descent / re-entry corridor** shall enforce a “slow, shallow” profile such that: (a) sustained deceleration remains within the TR‑2 bands (≤ 4 g sustained, ≤ 5 g short peaks), and (b) dynamic pressure during descent remains **≤ 60 kPa**, with a design target of **≤ 40 kPa** through the bulk of the sensible atmosphere. | Encodes the “slow descent” concept from `specs/mission-profile.md` §6; final limits to be tuned with aero/thermal analysis. Verification requires a descent/entry model with G and \( q \) histories; until then, these act as design targets for guidance and mass/aero trades. |

In practice, TR‑3/4 should be evaluated together with TR‑1/2: candidate mass, thrust, and Isp combinations from `specs/mass-and-propulsion.md` are acceptable only if a trajectory can be found that simultaneously satisfies the apogee band, G-limits, and these dynamic-pressure caps.

