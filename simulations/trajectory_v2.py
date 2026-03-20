#!/usr/bin/env python3
"""
Trajectory V2 — Concept V1 suborbital spaceplane with dynamic pressure.

Extends trajectory_v1.py with:
  - Standard atmosphere model (density vs. altitude).
  - Dynamic pressure q = 0.5 * rho * v^2 computed at each time step.
  - Outputs time, alt, mach, g_load, q_kPa for verification against TR-1/2/3.

Aligns with:
  - specs/mission-profile.md
  - specs/trajectory-requirements.md
  - specs/mass-and-propulsion.md

Simplified 1-D point-mass ascent:
  Phase 1: Air-breathing climb 0 → 25 km, Mach ~2 at handover.
  Phase 2: Rocket burn (nominal delta-V), then coast to apogee.

Verification gates:
  - TR-1: Apogee in 80–100 km
  - TR-2: Max G ≤ 4 g sustained, ≤ 5 g short peaks
  - TR-3: Max dynamic pressure q_max ≤ 60 kPa ascent (target ≤ 40 kPa low alt)
"""

import math
import csv
import os

# Constants
R_EARTH = 6.371e6   # m
G0 = 9.81            # m/s^2
GAMMA_AIR = 1.4
R_AIR = 287.0        # J/(kg·K)

def standard_atmosphere(alt_m):
    """
    US Standard Atmosphere 1976 simplified.
    Returns: (temperature_K, pressure_Pa, density_kg_m3)
    Valid up to ~50 km.
    """
    alt_km = alt_m / 1000.0
    
    # Sea level
    T0 = 288.15  # K
    P0 = 101325.0  # Pa
    
    # Troposphere (0–11 km): linear temp decrease
    if alt_km <= 11.0:
        T = T0 - 6.5 * alt_km
        P = P0 * (T / T0) ** 5.2561
    # Tropopause/Lower stratosphere (11–25 km): isothermal then warming
    elif alt_km <= 25.0:
        T = 216.65  # K (isothermal)
        P = 22632.0 * math.exp(-0.0001577 * (alt_m - 11000))
    # Stratosphere (25–47 km): warming
    elif alt_km <= 47.0:
        T = 216.65 + 2.8 * (alt_km - 25.0)
        P = 2488.4 * (T / 216.65) ** (-11.388)
    else:
        # Above 47 km: crude extrapolation
        T = 270.65
        P = 110.9 * math.exp(-0.0001262 * (alt_m - 47000))
    
    rho = P / (R_AIR * T) if T > 0 else 0.0
    return T, P, rho

def speed_of_sound(T_K):
    """Speed of sound (m/s) from temperature (K)."""
    return math.sqrt(GAMMA_AIR * R_AIR * T_K)

def run_trajectory():
    """
    Run simplified 1-D ascent trajectory with dynamic pressure computation.
    Returns: (rows, apogee_km, max_g, max_q_kPa)
    where rows = [(time_s, alt_km, mach, g_load, q_kPa), ...]
    """
    dt = 1.0   # s
    t = 0.0
    alt_m = 0.0
    v_ms = 0.0
    
    rows = []
    
    # Phase 1: Air-breathing climb 0 → 25 km over 300 s
    # Target: 25 km altitude, ~600 m/s velocity at handover
    t_phase1 = 300.0
    alt_handover_km = 25.0
    v_handover_ms = 600.0
    
    # Linear acceleration profile for simplicity
    accel_phase1 = v_handover_ms / t_phase1  # constant acceleration
    climb_rate_0 = 0.0
    climb_rate_end = 2 * (alt_handover_km * 1000) / t_phase1
    
    while t < t_phase1:
        # Linear velocity increase
        v_ms = (t / t_phase1) * v_handover_ms
        # Quadratic altitude (constant accel)
        alt_m = 0.5 * accel_phase1 * t * t
        alt_km = alt_m / 1000.0
        
        # Atmosphere
        T, P, rho = standard_atmosphere(alt_m)
        a_sound = speed_of_sound(T)
        mach = v_ms / a_sound if a_sound > 0 else 0.0
        
        # Dynamic pressure
        q_Pa = 0.5 * rho * v_ms * v_ms
        q_kPa = q_Pa / 1000.0
        
        # G-load (simplified: climb acceleration + gravity)
        accel_ms2 = accel_phase1
        g_load = 1.0 + accel_ms2 / G0
        
        rows.append((t, alt_km, mach, g_load, q_kPa))
        t += dt
    
    # At handover: 25 km, 600 m/s
    alt_m = alt_handover_km * 1000
    v_ms = v_handover_ms
    
    # Phase 2: Rocket burn
    # Target: +200 m/s delta-V over 60 s
    # This was tuned in V1 to reach ~100 km apogee
    burn_duration = 60.0
    dv_rocket = 200.0  # m/s
    accel_burn = dv_rocket / burn_duration  # constant thrust assumption
    
    t_burn_end = t + burn_duration
    while t < t_burn_end:
        v_ms += accel_burn * dt
        alt_m += v_ms * dt
        alt_km = alt_m / 1000.0
        
        T, P, rho = standard_atmosphere(alt_m)
        a_sound = speed_of_sound(T)
        mach = v_ms / a_sound if a_sound > 0 else 0.0
        
        q_Pa = 0.5 * rho * v_ms * v_ms
        q_kPa = q_Pa / 1000.0
        
        g_load = 1.0 + accel_burn / G0
        
        rows.append((t, alt_km, mach, g_load, q_kPa))
        t += dt
    
    # Phase 3: Coast to apogee
    while v_ms > 0:
        v_ms -= G0 * dt
        if v_ms < 0:
            v_ms = 0
        alt_m += v_ms * dt
        alt_km = alt_m / 1000.0
        
        T, P, rho = standard_atmosphere(alt_m)
        a_sound = speed_of_sound(T)
        mach = v_ms / a_sound if a_sound > 0 else 0.0
        
        q_Pa = 0.5 * rho * v_ms * v_ms
        q_kPa = q_Pa / 1000.0
        
        g_load = 1.0  # freefall
        
        rows.append((t, alt_km, mach, g_load, q_kPa))
        t += dt
        
        # Safety stop
        if alt_km > 150 or t > 2000:
            break
    
    apogee_km = max(r[1] for r in rows)
    max_g = max(r[3] for r in rows)
    max_q_kPa = max(r[4] for r in rows)
    
    return rows, apogee_km, max_g, max_q_kPa

def main():
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "trajectory_run_2.csv")
    summary_path = os.path.join(out_dir, "trajectory_run_2_summary.txt")
    
    print("Running trajectory V2 with dynamic pressure computation...")
    rows, apogee_km, max_g, max_q_kPa = run_trajectory()
    
    # Write CSV
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["time_s", "alt_km", "mach", "g_load", "q_kPa"])
        for row in rows:
            w.writerow([f"{row[0]:.1f}", f"{row[1]:.3f}", f"{row[2]:.3f}", 
                       f"{row[3]:.3f}", f"{row[4]:.3f}"])
    
    # Verification against TR-1, TR-2, TR-3
    tr1_pass = 80 <= apogee_km <= 100
    tr2_pass = max_g <= 5.0  # Short peak limit; sustained would need time-series analysis
    tr3_pass = max_q_kPa <= 60.0  # Draft limit from trajectory-requirements.md
    tr3_target = max_q_kPa <= 40.0  # Design target
    
    # Write summary
    with open(summary_path, "w") as f:
        f.write("Trajectory Run 2 — Concept V1 with Dynamic Pressure\n")
        f.write("=" * 60 + "\n\n")
        f.write("Mission profile: specs/mission-profile.md\n")
        f.write("Requirements:    specs/trajectory-requirements.md\n\n")
        
        f.write("RESULTS:\n")
        f.write(f"  Apogee:            {apogee_km:.2f} km\n")
        f.write(f"  Max G-load:        {max_g:.2f} g\n")
        f.write(f"  Max dynamic press: {max_q_kPa:.2f} kPa\n\n")
        
        f.write("VERIFICATION:\n")
        f.write(f"  TR-1 (Apogee 80-100 km):     {'PASS' if tr1_pass else 'FAIL'}\n")
        f.write(f"  TR-2 (G ≤ 5 g peak):         {'PASS' if tr2_pass else 'FAIL'}\n")
        f.write(f"  TR-3 (q_max ≤ 60 kPa):       {'PASS' if tr3_pass else 'FAIL'}\n")
        f.write(f"  TR-3 target (q ≤ 40 kPa):    {'PASS' if tr3_target else 'FAIL (design target)'}\n\n")
        
        f.write("NOTES:\n")
        f.write("  - This is a 1-D point-mass model with simplified atmosphere.\n")
        f.write("  - Drag not yet modeled; actual q profile will differ.\n")
        f.write("  - TR-2 sustained G check (≤4 g) requires time-series analysis.\n")
        f.write("  - TR-4 (descent/re-entry) not yet modeled.\n")
    
    # Console output
    print(f"\nApogee:      {apogee_km:.2f} km")
    print(f"Max G:       {max_g:.2f} g")
    print(f"Max q:       {max_q_kPa:.2f} kPa")
    print(f"\nTR-1: {'PASS' if tr1_pass else 'FAIL'}")
    print(f"TR-2: {'PASS' if tr2_pass else 'FAIL'}")
    print(f"TR-3: {'PASS' if tr3_pass else 'FAIL'}")
    print(f"\nOutput written to:")
    print(f"  {csv_path}")
    print(f"  {summary_path}")
    
    # Exit code: 0 if all pass, 1 otherwise
    all_pass = tr1_pass and tr2_pass and tr3_pass
    return 0 if all_pass else 1

if __name__ == "__main__":
    exit(main())
