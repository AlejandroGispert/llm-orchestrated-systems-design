#!/usr/bin/env python3
"""
Trajectory Sensitivity Study — Concept V1

Explores how trajectory outcomes (apogee, max G, max q) respond to variations
in key design parameters from specs/mass-and-propulsion.md:
  - Rocket Δv (1.0–1.5 km/s)
  - Rocket burn time (40–80 s) → affects T/W
  - Air-breathing handover conditions (20–30 km, 500–700 m/s)

Runs multiple trajectory cases with trajectory_v2-style physics (1-D point-mass
with standard atmosphere and dynamic pressure) and outputs:
  - CSV table of parameter combinations and outcomes
  - Summary analysis for TR-1/2/3 gate violations
  - Recommendations for design space narrowing

Aligns with:
  - specs/mass-and-propulsion.md §3 (rocket Δv and T/W bands)
  - specs/trajectory-requirements.md (TR-1/2/3 verification gates)
  - Next priority in docs/JOURNAL.md
"""

import math
import csv
import os
import itertools

# Constants
R_EARTH = 6.371e6   # m
G0 = 9.81            # m/s^2
GAMMA_AIR = 1.4
R_AIR = 287.0        # J/(kg·K)

def standard_atmosphere(alt_m):
    """US Standard Atmosphere 1976 simplified."""
    alt_km = alt_m / 1000.0
    T0, P0 = 288.15, 101325.0
    
    if alt_km <= 11.0:
        T = T0 - 6.5 * alt_km
        P = P0 * (T / T0) ** 5.2561
    elif alt_km <= 25.0:
        T = 216.65
        P = 22632.0 * math.exp(-0.0001577 * (alt_m - 11000))
    elif alt_km <= 47.0:
        T = 216.65 + 2.8 * (alt_km - 25.0)
        P = 2488.4 * (T / 216.65) ** (-11.388)
    else:
        T = 270.65
        P = 110.9 * math.exp(-0.0001262 * (alt_m - 47000))
    
    rho = P / (R_AIR * T) if T > 0 else 0.0
    return T, P, rho

def speed_of_sound(T_K):
    """Speed of sound (m/s)."""
    return math.sqrt(GAMMA_AIR * R_AIR * T_K)

def run_trajectory_case(handover_alt_km, handover_vel_ms, rocket_dv_ms, burn_time_s):
    """
    Run single trajectory case with specified parameters.
    
    Returns: (apogee_km, max_g, max_q_kPa, tr1_pass, tr2_pass, tr3_pass)
    """
    dt = 1.0
    t = 0.0
    
    # Phase 1: Air-breathing climb to handover
    # Simplified: linear velocity and altitude growth over 300 s
    t_phase1 = 300.0
    
    alt_m = 0.0
    v_ms = 0.0
    
    max_g = 1.0
    max_q_kPa = 0.0
    
    # Air-breathing phase
    while t < t_phase1:
        v_ms = (t / t_phase1) * handover_vel_ms
        accel_ms2 = handover_vel_ms / t_phase1
        alt_m = 0.5 * accel_ms2 * t * t
        
        T, P, rho = standard_atmosphere(alt_m)
        a_sound = speed_of_sound(T)
        q_Pa = 0.5 * rho * v_ms * v_ms
        q_kPa = q_Pa / 1000.0
        g_load = 1.0 + accel_ms2 / G0
        
        max_g = max(max_g, g_load)
        max_q_kPa = max(max_q_kPa, q_kPa)
        
        t += dt
    
    # Set handover state
    alt_m = handover_alt_km * 1000
    v_ms = handover_vel_ms
    
    # Phase 2: Rocket burn
    accel_burn = rocket_dv_ms / burn_time_s
    t_burn_end = t + burn_time_s
    
    while t < t_burn_end:
        v_ms += accel_burn * dt
        alt_m += v_ms * dt
        
        T, P, rho = standard_atmosphere(alt_m)
        a_sound = speed_of_sound(T)
        q_Pa = 0.5 * rho * v_ms * v_ms
        q_kPa = q_Pa / 1000.0
        g_load = 1.0 + accel_burn / G0
        
        max_g = max(max_g, g_load)
        max_q_kPa = max(max_q_kPa, q_kPa)
        
        t += dt
    
    # Phase 3: Coast to apogee
    while v_ms > 0:
        v_ms -= G0 * dt
        if v_ms < 0:
            v_ms = 0
        alt_m += v_ms * dt
        
        T, P, rho = standard_atmosphere(alt_m)
        q_Pa = 0.5 * rho * v_ms * v_ms
        q_kPa = q_Pa / 1000.0
        
        max_q_kPa = max(max_q_kPa, q_kPa)
        
        t += dt
        
        if alt_m / 1000.0 > 150 or t > 2000:
            break
    
    apogee_km = alt_m / 1000.0
    
    # Verification gates
    tr1_pass = 80 <= apogee_km <= 100
    tr2_pass = max_g <= 5.0  # Peak limit
    tr3_pass = max_q_kPa <= 60.0  # Ascent limit
    
    return apogee_km, max_g, max_q_kPa, tr1_pass, tr2_pass, tr3_pass

def main():
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)
    
    csv_path = os.path.join(out_dir, "trajectory_sensitivity.csv")
    summary_path = os.path.join(out_dir, "trajectory_sensitivity_summary.txt")
    
    print("Running trajectory sensitivity study...")
    print("Exploring design space from specs/mass-and-propulsion.md\n")
    
    # Design parameter ranges
    # From specs/mass-and-propulsion.md §3:
    #   - Rocket Δv: 1.0–1.5 km/s
    #   - Burn time: 40–80 s (affects T/W)
    # From specs/mission-profile.md §2:
    #   - Handover: 25–30 km, Mach 4–6 (~600 m/s at those altitudes)
    
    handover_alts_km = [20, 25, 30]
    handover_vels_ms = [500, 600, 700]
    rocket_dvs_ms = [1000, 1200, 1500]  # 1.0, 1.2, 1.5 km/s
    burn_times_s = [40, 60, 80]
    
    cases = []
    all_pass_count = 0
    total_count = 0
    
    for h_alt, h_vel, r_dv, b_time in itertools.product(
        handover_alts_km, handover_vels_ms, rocket_dvs_ms, burn_times_s
    ):
        result = run_trajectory_case(h_alt, h_vel, r_dv, b_time)
        apogee_km, max_g, max_q_kPa, tr1, tr2, tr3 = result
        
        all_pass = tr1 and tr2 and tr3
        if all_pass:
            all_pass_count += 1
        total_count += 1
        
        # Compute effective T/W at burn start (approx, ignoring mass change)
        # T/W = accel / g0, where accel = dv / burn_time
        tw_equiv = (r_dv / b_time) / G0
        
        cases.append({
            'handover_alt_km': h_alt,
            'handover_vel_ms': h_vel,
            'rocket_dv_ms': r_dv,
            'burn_time_s': b_time,
            'tw_equiv': tw_equiv,
            'apogee_km': apogee_km,
            'max_g': max_g,
            'max_q_kPa': max_q_kPa,
            'tr1_pass': tr1,
            'tr2_pass': tr2,
            'tr3_pass': tr3,
            'all_pass': all_pass
        })
    
    # Write CSV
    with open(csv_path, 'w', newline='') as f:
        fieldnames = ['handover_alt_km', 'handover_vel_ms', 'rocket_dv_ms', 
                     'burn_time_s', 'tw_equiv', 'apogee_km', 'max_g', 'max_q_kPa',
                     'tr1_pass', 'tr2_pass', 'tr3_pass', 'all_pass']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for c in cases:
            w.writerow(c)
    
    # Analysis
    passing_cases = [c for c in cases if c['all_pass']]
    
    # Find best case (middle of apogee band, lowest max_g, lowest max_q)
    if passing_cases:
        # Score: distance from 90 km apogee + penalty for high G and q
        for c in passing_cases:
            c['score'] = (
                abs(c['apogee_km'] - 90.0) +
                0.2 * max(0, c['max_g'] - 3.0) +  # Prefer G < 3
                0.1 * max(0, c['max_q_kPa'] - 30.0)  # Prefer q < 30 kPa
            )
        best = min(passing_cases, key=lambda x: x['score'])
    else:
        best = None
    
    # Write summary
    with open(summary_path, 'w') as f:
        f.write("Trajectory Sensitivity Study — Concept V1\n")
        f.write("=" * 70 + "\n\n")
        f.write("Objective: Explore how apogee, max G, and max q respond to\n")
        f.write("           variations in handover conditions, rocket Δv, and burn time.\n\n")
        
        f.write(f"PARAMETER RANGES TESTED:\n")
        f.write(f"  Handover altitude: {handover_alts_km} km\n")
        f.write(f"  Handover velocity: {handover_vels_ms} m/s\n")
        f.write(f"  Rocket Δv:         {[x/1000 for x in rocket_dvs_ms]} km/s\n")
        f.write(f"  Burn time:         {burn_times_s} s\n")
        f.write(f"  Total cases:       {total_count}\n\n")
        
        f.write(f"RESULTS:\n")
        f.write(f"  Cases passing all gates (TR-1/2/3): {all_pass_count}/{total_count}\n")
        f.write(f"  Success rate:                       {100*all_pass_count/total_count:.1f}%\n\n")
        
        if best:
            f.write(f"RECOMMENDED NOMINAL CASE (best score among passing):\n")
            f.write(f"  Handover:    {best['handover_alt_km']} km, {best['handover_vel_ms']} m/s\n")
            f.write(f"  Rocket Δv:   {best['rocket_dv_ms']/1000:.1f} km/s\n")
            f.write(f"  Burn time:   {best['burn_time_s']} s\n")
            f.write(f"  T/W equiv:   {best['tw_equiv']:.2f}\n")
            f.write(f"  → Apogee:    {best['apogee_km']:.1f} km\n")
            f.write(f"  → Max G:     {best['max_g']:.2f} g\n")
            f.write(f"  → Max q:     {best['max_q_kPa']:.1f} kPa\n\n")
        else:
            f.write("WARNING: No cases passed all gates. Design space may need expansion.\n\n")
        
        f.write("FAILURE MODES (if any):\n")
        tr1_fails = [c for c in cases if not c['tr1_pass']]
        tr2_fails = [c for c in cases if not c['tr2_pass']]
        tr3_fails = [c for c in cases if not c['tr3_pass']]
        
        f.write(f"  TR-1 violations (apogee out of 80-100 km): {len(tr1_fails)}\n")
        if tr1_fails:
            apogees = [c['apogee_km'] for c in tr1_fails]
            f.write(f"    Apogee range in failures: {min(apogees):.1f}–{max(apogees):.1f} km\n")
        
        f.write(f"  TR-2 violations (G > 5):                   {len(tr2_fails)}\n")
        if tr2_fails:
            gs = [c['max_g'] for c in tr2_fails]
            f.write(f"    Max G in failures: {max(gs):.2f} g\n")
        
        f.write(f"  TR-3 violations (q > 60 kPa):              {len(tr3_fails)}\n")
        if tr3_fails:
            qs = [c['max_q_kPa'] for c in tr3_fails]
            f.write(f"    Max q in failures: {max(qs):.1f} kPa\n")
        
        f.write("\nKEY INSIGHTS:\n")
        
        # Analyze trends
        if passing_cases:
            avg_apogee = sum(c['apogee_km'] for c in passing_cases) / len(passing_cases)
            avg_g = sum(c['max_g'] for c in passing_cases) / len(passing_cases)
            avg_q = sum(c['max_q_kPa'] for c in passing_cases) / len(passing_cases)
            
            f.write(f"  - Average outcomes for passing cases:\n")
            f.write(f"      Apogee: {avg_apogee:.1f} km, Max G: {avg_g:.2f} g, Max q: {avg_q:.1f} kPa\n")
            
            # Check if rocket dv matters
            dv_groups = {}
            for c in passing_cases:
                dv_groups.setdefault(c['rocket_dv_ms'], []).append(c['apogee_km'])
            f.write(f"  - Rocket Δv vs apogee correlation:\n")
            for dv in sorted(dv_groups.keys()):
                avg = sum(dv_groups[dv]) / len(dv_groups[dv])
                f.write(f"      {dv/1000:.1f} km/s → avg apogee {avg:.1f} km\n")
        
        f.write("\nNEXT STEPS:\n")
        f.write("  1. Update specs/mass-and-propulsion.md with narrowed parameter bands\n")
        f.write("     based on passing cases (if success rate high).\n")
        f.write("  2. Refine trajectory_v2.py with drag model to improve q and G predictions.\n")
        f.write("  3. Add descent/re-entry phase for TR-4 verification.\n")
        f.write("  4. Capture insights in docs/LEARNINGS.md.\n")
    
    # Console output
    print(f"Cases tested:  {total_count}")
    print(f"All gates pass: {all_pass_count} ({100*all_pass_count/total_count:.1f}%)")
    if best:
        print(f"\nRecommended nominal:")
        print(f"  Handover: {best['handover_alt_km']} km @ {best['handover_vel_ms']} m/s")
        print(f"  Rocket:   {best['rocket_dv_ms']/1000:.1f} km/s over {best['burn_time_s']} s")
        print(f"  Outcomes: apogee {best['apogee_km']:.1f} km, G {best['max_g']:.2f}, q {best['max_q_kPa']:.1f} kPa")
    
    print(f"\nOutput written to:")
    print(f"  {csv_path}")
    print(f"  {summary_path}")
    
    return 0

if __name__ == "__main__":
    exit(main())
