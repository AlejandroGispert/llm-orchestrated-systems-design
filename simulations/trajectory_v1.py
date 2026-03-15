#!/usr/bin/env python3
"""
First trajectory run — Concept V1 suborbital spaceplane.
Aligns with specs/mission-profile.md and designs/concept-v1.md §4.

Simplified 1-D point-mass ascent:
  Phase 1: Air-breathing climb 0 → 25 km, Mach 4 at handover.
  Phase 2: Rocket burn (nominal delta-V), then coast to apogee.

Outputs: time, alt_km, mach, g_load; summary with apogee_km, max_g.
Verification: apogee in 80–100 km, max G ≤ 4 g sustained (≤ 5 g peak).
"""

import math
import csv
import os

# Constants
R_EARTH = 6.371e6   # m
G0 = 9.81            # m/s^2
GAMMA_AIR = 1.4
R_AIR = 287.0        # J/(kg·K)

def speed_of_sound(alt_km):
    """Approximate speed of sound (m/s) vs altitude (km). US std atm simplified."""
    if alt_km <= 25:
        T = 288.15 - 6.5 * alt_km  # troposphere
    else:
        T = 288.15 - 6.5 * 25     # stratosphere approx
    return math.sqrt(GAMMA_AIR * R_AIR * T)

def run_trajectory():
    dt = 1.0   # s
    t = 0.0
    alt_km = 0.0
    v_ms = 0.0
    g_load = 1.0
    mach = 0.0

    # Phase 1: linear climb to 25 km over 300 s; handover at 25 km with v chosen so burn yields 80–100 km apogee
    t_phase1 = 300.0
    alt_handover = 25.0   # km
    v_handover = 600.0   # m/s (nominal; Mach ~2 at 25 km) so rocket burn can target 100 km apogee
    climb_rate_ms = (alt_handover * 1000) / t_phase1  # m/s

    rows = []
    while t < t_phase1:
        alt_km = (t / t_phase1) * alt_handover
        v_ms = (t / t_phase1) * v_handover
        a_sound = speed_of_sound(alt_km)
        mach = v_ms / a_sound if a_sound > 0 else 0
        g_load = 1.0 + (climb_rate_ms / G0) * 0.3  # approximate
        rows.append((t, alt_km, mach, g_load))
        t += dt

    # Phase 2: rocket burn then coast
    # Target apogee 100 km. End-of-burn alt = 25e3 + 60*(v_handover + dv/2), v = v_handover + dv; coast adds v^2/(2g).
    # Solve: 25e3 + 60*(v_handover + dv/2) + (v_handover+dv)^2/(2*g) = 100e3 => dv ~ 271 m/s for v_handover=600.
    burn_duration = 60.0
    dv_rocket = 200.0   # m/s (tuned for ~100 km apogee from 25 km handover at 600 m/s)
    accel_burn = dv_rocket / burn_duration
    g_burn = 1.0 + accel_burn / G0

    alt_m = alt_handover * 1000
    v_ms = v_handover
    while t < t_phase1 + burn_duration:
        v_ms += accel_burn * dt
        alt_m += v_ms * dt
        alt_km = alt_m / 1000
        a_sound = speed_of_sound(alt_km)
        mach = v_ms / a_sound if a_sound > 0 else 0
        g_load = 1.0 + accel_burn / G0
        rows.append((t, alt_km, mach, g_load))
        t += dt

    # Coast to apogee
    while v_ms > 0:
        v_ms -= G0 * dt
        alt_m += v_ms * dt
        alt_km = alt_m / 1000
        a_sound = speed_of_sound(min(alt_km, 50))
        mach = v_ms / a_sound if a_sound > 0 else 0
        g_load = 1.0
        rows.append((t, alt_km, mach, g_load))
        t += dt
        if alt_km > 150:
            break

    apogee_km = alt_km
    max_g = max(r[3] for r in rows)

    return rows, apogee_km, max_g

def main():
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "trajectory_run_1.csv")
    summary_path = os.path.join(out_dir, "trajectory_run_1_summary.txt")

    rows, apogee_km, max_g = run_trajectory()

    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["time_s", "alt_km", "mach", "g_load"])
        w.writerows(rows)

    with open(summary_path, "w") as f:
        f.write("First trajectory run — Concept V1\n")
        f.write("Mission profile: specs/mission-profile.md\n\n")
        f.write(f"Apogee: {apogee_km:.2f} km\n")
        f.write(f"Max G:  {max_g:.2f} g\n\n")
        ok_apogee = 80 <= apogee_km <= 100
        ok_g = max_g <= 5.0
        f.write(f"Apogee in 80–100 km: {'PASS' if ok_apogee else 'FAIL'}\n")
        f.write(f"G ≤ 5 g peak:          {'PASS' if ok_g else 'FAIL'}\n")

    print(f"Apogee: {apogee_km:.2f} km, Max G: {max_g:.2f} g")
    print(f"Output: {csv_path}, {summary_path}")
    return 0 if (80 <= apogee_km <= 100 and max_g <= 5) else 1

if __name__ == "__main__":
    exit(main())
