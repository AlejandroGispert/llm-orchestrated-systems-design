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

### 2. Future Aero / Dynamic-Pressure Gates (Placeholder)

These are **placeholders** to be turned into hard requirements once a coupled aero model is introduced:

| ID | Requirement (draft) | Notes |
|----|---------------------|-------|
| TR-3 (draft) | Maximum dynamic pressure \( q_\text{max} \) during ascent shall not exceed a TBD limit consistent with structural and TPS design. | Requires adding atmosphere and aero modeling (e.g., \( q = \tfrac{1}{2}\rho V^2 \)) to the trajectory solver. |
| TR-4 (draft) | Re-entry corridor shall enforce a “slow descent” profile with combined G and \( q \) kept within crew comfort and structural limits. | To be refined once a descent/entry model is implemented. |

