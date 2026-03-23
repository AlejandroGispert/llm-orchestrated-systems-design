#!/usr/bin/env python3
"""
Trajectory Simulation — Segment A (Air-breathing Climb)

Models the air-breathing climb phase from takeoff to handover conditions
(~25-30 km altitude, 500-700 m/s velocity) using the T/W and fuel fraction
bands specified in specs/mass-and-propulsion.md.

Purpose:
- Verify that handover conditions are achievable with specified T/W bands
- Quantify fuel consumption and time-to-handover
- Check dynamic pressure and G-loads during climb
- Validate "slow ascent" philosophy

Gates:
- Handover altitude: 25-30 km
- Handover velocity: 500-700 m/s
- Max G-load: ≤4 g sustained, ≤5 g peak
- Max dynamic pressure: ≤40 kPa (design target from trajectory-requirements.md)

Simplifications (conceptual phase):
- 2-D point-mass dynamics (vertical + horizontal)
- Simplified drag model (constant C_D × reference area)
- Exponential atmosphere
- Constant specific fuel consumption (SFC) for air-breathing propulsion
- Neglects propulsive efficiency variations with altitude/Mach
- No detailed propulsion cycle modeling
- Starts from liftoff velocity (not ground roll)

Author: aerospace conceptual design agent
Date: Day 8 (2026-03-23)
"""

import numpy as np
import sys

# ============================================================================
# CONSTANTS
# ============================================================================

g0 = 9.80665  # m/s² — standard gravity
R_EARTH = 6371e3  # m — Earth radius (for altitude correction if needed)

# Atmospheric model (exponential approximation)
RHO_0 = 1.225  # kg/m³ — sea level density
H_SCALE = 8500.0  # m — scale height

def atmosphere_density(h):
    """Return atmospheric density at altitude h (m) using exponential model."""
    return RHO_0 * np.exp(-h / H_SCALE)

def atmosphere_pressure(h):
    """Return atmospheric pressure at altitude h (m)."""
    P_0 = 101325.0  # Pa
    return P_0 * np.exp(-h / H_SCALE)

# ============================================================================
# VEHICLE PARAMETERS (from specs/mass-and-propulsion.md)
# ============================================================================

# Mass budget
m_0 = 10000.0  # kg — reference gross liftoff mass (GLOW)
fuel_frac_AB = 0.10  # 10% — air-breathing fuel fraction (8-12% band, nominal)
m_fuel_AB = m_0 * fuel_frac_AB

# Propulsion (Segment A)
T_W_sea_level = 0.55  # Sea-level T/W (0.4-0.7 band, nominal)
T_W_high_alt = 0.30   # High-altitude T/W at 25-30 km (0.2-0.4 band, nominal)

# Thrust variation with altitude (simplified model)
# Assume thrust decreases roughly with density for air-breathing engines
def thrust_air_breathing(h, m_current):
    """
    Return thrust (N) at altitude h for current vehicle mass.
    
    Model: Thrust scales with atmospheric density relative to sea level,
    interpolated between sea-level and high-altitude T/W targets.
    """
    rho_ratio = atmosphere_density(h) / RHO_0
    
    # Interpolate T/W based on density ratio (simplified)
    # At sea level: T/W = T_W_sea_level
    # At 25-30 km (rho_ratio ~ 0.01-0.02): T/W = T_W_high_alt
    
    # For simplicity, scale thrust with rho_ratio to maintain reasonable climb capability
    # This is a crude approximation; real turbojets/ramjets have complex performance curves
    T_W_effective = T_W_sea_level * (rho_ratio ** 0.5)  # sqrt scaling as compromise
    T_W_effective = max(T_W_effective, T_W_high_alt * 0.5)  # floor to maintain some thrust
    
    return T_W_effective * m_current * g0

# Specific fuel consumption (crude approximation)
SFC = 0.8e-4  # kg/(N·s) — order of magnitude for jet engines (TSFC ~ 0.8-1.2 lb/(lbf·hr) → 0.8-1.2e-4 kg/(N·s))

# Aerodynamics (very simplified)
S_ref = 50.0  # m² — reference wing area (placeholder for conceptual sizing)
C_D = 0.04    # Drag coefficient (low-drag cruise configuration; will vary with AoA, Mach)
L_over_D = 8.0  # Lift-to-drag ratio during climb (placeholder; will vary with flight regime)

def drag_force(h, v):
    """Return drag force (N) at altitude h and velocity v."""
    rho = atmosphere_density(h)
    q = 0.5 * rho * v**2
    return C_D * S_ref * q

def lift_force(h, v):
    """Return lift force (N) at altitude h and velocity v."""
    rho = atmosphere_density(h)
    q = 0.5 * rho * v**2
    C_L = C_D * L_over_D
    return C_L * S_ref * q

# ============================================================================
# SIMULATION PARAMETERS
# ============================================================================

dt = 1.0  # s — time step
t_max = 1200.0  # s — maximum simulation time (20 minutes)

# Target handover conditions
h_handover_min = 25000.0  # m
h_handover_max = 30000.0  # m
v_handover_min = 500.0    # m/s
v_handover_max = 700.0    # m/s

# G-load limits
G_limit_sustained = 4.0
G_limit_peak = 5.0

# Dynamic pressure limit (design target)
q_limit = 40000.0  # Pa (40 kPa)

# ============================================================================
# TRAJECTORY INTEGRATION
# ============================================================================

def simulate_segment_a():
    """
    Simulate air-breathing climb from takeoff to handover conditions.
    
    Returns:
        trajectory: dict with time-series data
        summary: dict with key results and gate checks
    """
    
    # Initial conditions (post-liftoff)
    t = 0.0
    h = 10.0       # m — altitude (just after liftoff)
    v = 70.0       # m/s — liftoff velocity (~140 knots, typical for aircraft)
    gamma = 15.0 * np.pi / 180.0  # rad — initial climb angle (moderate)
    
    m_current = m_0  # kg
    m_fuel_remaining = m_fuel_AB
    
    # Storage
    time_history = [t]
    h_history = [h]
    v_history = [v]
    gamma_history = [gamma]
    m_history = [m_current]
    fuel_history = [m_fuel_remaining]
    G_history = [1.0]
    q_history = [0.5 * atmosphere_density(h) * v**2]
    T_history = [thrust_air_breathing(h, m_current)]
    
    # Max values for gate checks
    G_max = 1.0
    q_max = 0.5 * atmosphere_density(h) * v**2
    
    handover_reached = False
    reason = "Unknown"
    
    # Main integration loop
    while t < t_max:
        
        # Current forces
        T = thrust_air_breathing(h, m_current)
        D = drag_force(h, v)
        L = lift_force(h, v)
        W = m_current * g0
        
        # Equations of motion (2-D point-mass, flat Earth)
        # dv/dt = (T - D) / m - g * sin(gamma)
        # dh/dt = v * sin(gamma)
        # d(gamma)/dt = (L - W*cos(gamma)) / (m * v) (centripetal + gravity turn)
        
        # Net acceleration parallel to velocity
        a_parallel = (T - D) / m_current - g0 * np.sin(gamma)
        
        # Normal acceleration (perpendicular to velocity)
        # For subsonic-to-supersonic climb, approximate with lift balance
        a_normal = (L - W * np.cos(gamma)) / m_current
        gamma_dot = a_normal / v if v > 1.0 else 0.0
        
        # Fuel consumption
        fuel_rate = SFC * T  # kg/s
        
        # Integration (Euler method)
        v_new = v + a_parallel * dt
        h_new = h + v * np.sin(gamma) * dt
        gamma_new = gamma + gamma_dot * dt
        m_fuel_remaining -= fuel_rate * dt
        m_current = m_0 - (m_fuel_AB - m_fuel_remaining)
        
        # Clamp flight path angle to reasonable bounds
        gamma_new = np.clip(gamma_new, -10.0 * np.pi / 180.0, 60.0 * np.pi / 180.0)
        
        # Prevent negative velocity or altitude
        if v_new < 0 or h_new < 0:
            reason = "Unphysical state (negative altitude or velocity)"
            break
        
        # Dynamic pressure and G-load
        rho = atmosphere_density(h_new)
        q = 0.5 * rho * v_new**2
        a_total = np.sqrt(a_parallel**2 + a_normal**2)
        G_load = a_total / g0
        
        # Update max values
        G_max = max(G_max, G_load)
        q_max = max(q_max, q)
        
        # Update state
        t += dt
        v = v_new
        h = h_new
        gamma = gamma_new
        
        # Store history
        time_history.append(t)
        h_history.append(h)
        v_history.append(v)
        gamma_history.append(gamma)
        m_history.append(m_current)
        fuel_history.append(m_fuel_remaining)
        G_history.append(G_load)
        q_history.append(q)
        T_history.append(T)
        
        # Check termination conditions
        
        # Out of fuel
        if m_fuel_remaining <= 0:
            reason = "Fuel exhausted"
            break
        
        # Handover conditions reached
        if (h_handover_min <= h <= h_handover_max and
            v_handover_min <= v <= v_handover_max):
            handover_reached = True
            reason = "Handover conditions reached"
            break
        
        # Overshot altitude without reaching velocity
        if h > h_handover_max + 5000.0:
            reason = "Altitude overshoot (insufficient velocity)"
            break
        
        # Overshot velocity without reaching altitude
        if v > v_handover_max + 100.0 and h < h_handover_min:
            reason = "Velocity overshoot (insufficient altitude)"
            break
    
    # End of simulation
    if t >= t_max:
        reason = "Maximum simulation time reached"
    
    # Build trajectory dict
    trajectory = {
        'time': np.array(time_history),
        'altitude': np.array(h_history),
        'velocity': np.array(v_history),
        'gamma': np.array(gamma_history),
        'mass': np.array(m_history),
        'fuel_remaining': np.array(fuel_history),
        'G_load': np.array(G_history),
        'q': np.array(q_history),
        'thrust': np.array(T_history),
    }
    
    # Gate checks
    gates = {
        'handover_reached': handover_reached,
        'altitude_in_range': h_handover_min <= h <= h_handover_max,
        'velocity_in_range': v_handover_min <= v <= v_handover_max,
        'G_sustained_ok': G_max <= G_limit_sustained,
        'G_peak_ok': G_max <= G_limit_peak,
        'q_ok': q_max <= q_limit,
    }
    
    all_gates_pass = all(gates.values())
    
    # Summary
    summary = {
        'handover_reached': handover_reached,
        'reason': reason,
        'final_time': t,
        'final_altitude': h,
        'final_velocity': v,
        'final_gamma_deg': gamma * 180.0 / np.pi,
        'final_mass': m_current,
        'fuel_consumed': m_fuel_AB - m_fuel_remaining,
        'fuel_consumed_frac': (m_fuel_AB - m_fuel_remaining) / m_0,
        'G_max': G_max,
        'q_max': q_max / 1000.0,  # kPa
        'gates': gates,
        'all_gates_pass': all_gates_pass,
    }
    
    return trajectory, summary

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    
    print("=" * 70)
    print("Segment A Trajectory Simulation — Air-Breathing Climb")
    print("=" * 70)
    print()
    
    print("Vehicle parameters:")
    print(f"  GLOW:                {m_0:.0f} kg")
    print(f"  Air-breathing fuel:  {m_fuel_AB:.0f} kg ({fuel_frac_AB*100:.1f}%)")
    print(f"  T/W (sea level):     {T_W_sea_level:.2f}")
    print(f"  T/W (high altitude): {T_W_high_alt:.2f}")
    print(f"  Reference area:      {S_ref:.1f} m²")
    print(f"  Drag coefficient:    {C_D:.3f}")
    print(f"  L/D ratio:           {L_over_D:.1f}")
    print()
    
    print("Target handover conditions:")
    print(f"  Altitude:  {h_handover_min/1000:.0f}-{h_handover_max/1000:.0f} km")
    print(f"  Velocity:  {v_handover_min:.0f}-{v_handover_max:.0f} m/s")
    print()
    
    print("Running simulation...")
    print()
    
    trajectory, summary = simulate_segment_a()
    
    print("=" * 70)
    print("Simulation Results")
    print("=" * 70)
    print()
    
    print(f"Handover reached:     {summary['handover_reached']}")
    print(f"Termination reason:   {summary['reason']}")
    print(f"Simulation time:      {summary['final_time']:.1f} s ({summary['final_time']/60:.1f} min)")
    print()
    
    print(f"Final state:")
    print(f"  Altitude:           {summary['final_altitude']/1000:.2f} km")
    print(f"  Velocity:           {summary['final_velocity']:.1f} m/s (Mach {summary['final_velocity']/340:.2f})")
    print(f"  Flight path angle:  {summary['final_gamma_deg']:.1f}°")
    print(f"  Mass:               {summary['final_mass']:.0f} kg")
    print()
    
    print(f"Fuel consumption:")
    print(f"  Consumed:           {summary['fuel_consumed']:.0f} kg ({summary['fuel_consumed_frac']*100:.1f}% of GLOW)")
    print(f"  Remaining:          {m_fuel_AB - summary['fuel_consumed']:.0f} kg")
    print()
    
    print(f"Max values during climb:")
    print(f"  G-load:             {summary['G_max']:.2f} g")
    print(f"  Dynamic pressure:   {summary['q_max']:.2f} kPa")
    print()
    
    print("=" * 70)
    print("Gate Checks")
    print("=" * 70)
    print()
    
    gates = summary['gates']
    print(f"  Handover reached:         {gates['handover_reached']}")
    print(f"  Altitude in range:        {gates['altitude_in_range']}")
    print(f"  Velocity in range:        {gates['velocity_in_range']}")
    print(f"  G sustained ok (≤4 g):    {gates['G_sustained_ok']}")
    print(f"  G peak ok (≤5 g):         {gates['G_peak_ok']}")
    print(f"  q ok (≤40 kPa):           {gates['q_ok']}")
    print()
    print(f"All gates PASS:             {summary['all_gates_pass']}")
    print()
    
    # Write output files
    import os
    os.makedirs("simulations/output", exist_ok=True)
    
    # CSV output
    csv_path = "simulations/output/trajectory_segment_a.csv"
    with open(csv_path, 'w') as f:
        f.write("time_s,altitude_m,velocity_m_s,gamma_deg,mass_kg,fuel_remaining_kg,G_load,q_Pa,thrust_N\n")
        for i in range(len(trajectory['time'])):
            f.write(f"{trajectory['time'][i]:.2f},")
            f.write(f"{trajectory['altitude'][i]:.2f},")
            f.write(f"{trajectory['velocity'][i]:.2f},")
            f.write(f"{trajectory['gamma'][i]*180/np.pi:.2f},")
            f.write(f"{trajectory['mass'][i]:.2f},")
            f.write(f"{trajectory['fuel_remaining'][i]:.2f},")
            f.write(f"{trajectory['G_load'][i]:.3f},")
            f.write(f"{trajectory['q'][i]:.2f},")
            f.write(f"{trajectory['thrust'][i]:.2f}\n")
    
    print(f"Trajectory data written to: {csv_path}")
    
    # Summary output
    summary_path = "simulations/output/trajectory_segment_a_summary.txt"
    with open(summary_path, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("Segment A Trajectory Simulation — Air-Breathing Climb\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("Vehicle parameters:\n")
        f.write(f"  GLOW:                {m_0:.0f} kg\n")
        f.write(f"  Air-breathing fuel:  {m_fuel_AB:.0f} kg ({fuel_frac_AB*100:.1f}%)\n")
        f.write(f"  T/W (sea level):     {T_W_sea_level:.2f}\n")
        f.write(f"  T/W (high altitude): {T_W_high_alt:.2f}\n")
        f.write(f"  Reference area:      {S_ref:.1f} m²\n")
        f.write(f"  Drag coefficient:    {C_D:.3f}\n")
        f.write(f"  L/D ratio:           {L_over_D:.1f}\n\n")
        
        f.write("Target handover conditions:\n")
        f.write(f"  Altitude:  {h_handover_min/1000:.0f}-{h_handover_max/1000:.0f} km\n")
        f.write(f"  Velocity:  {v_handover_min:.0f}-{v_handover_max:.0f} m/s\n\n")
        
        f.write("=" * 70 + "\n")
        f.write("Simulation Results\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Handover reached:     {summary['handover_reached']}\n")
        f.write(f"Termination reason:   {summary['reason']}\n")
        f.write(f"Simulation time:      {summary['final_time']:.1f} s ({summary['final_time']/60:.1f} min)\n\n")
        
        f.write(f"Final state:\n")
        f.write(f"  Altitude:           {summary['final_altitude']/1000:.2f} km\n")
        f.write(f"  Velocity:           {summary['final_velocity']:.1f} m/s (Mach {summary['final_velocity']/340:.2f})\n")
        f.write(f"  Flight path angle:  {summary['final_gamma_deg']:.1f}°\n")
        f.write(f"  Mass:               {summary['final_mass']:.0f} kg\n\n")
        
        f.write(f"Fuel consumption:\n")
        f.write(f"  Consumed:           {summary['fuel_consumed']:.0f} kg ({summary['fuel_consumed_frac']*100:.1f}% of GLOW)\n")
        f.write(f"  Remaining:          {m_fuel_AB - summary['fuel_consumed']:.0f} kg\n\n")
        
        f.write(f"Max values during climb:\n")
        f.write(f"  G-load:             {summary['G_max']:.2f} g\n")
        f.write(f"  Dynamic pressure:   {summary['q_max']:.2f} kPa\n\n")
        
        f.write("=" * 70 + "\n")
        f.write("Gate Checks\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"  Handover reached:         {gates['handover_reached']}\n")
        f.write(f"  Altitude in range:        {gates['altitude_in_range']}\n")
        f.write(f"  Velocity in range:        {gates['velocity_in_range']}\n")
        f.write(f"  G sustained ok (≤4 g):    {gates['G_sustained_ok']}\n")
        f.write(f"  G peak ok (≤5 g):         {gates['G_peak_ok']}\n")
        f.write(f"  q ok (≤40 kPa):           {gates['q_ok']}\n\n")
        f.write(f"All gates PASS:             {summary['all_gates_pass']}\n\n")
    
    print(f"Summary written to: {summary_path}")
    print()
    
    if summary['all_gates_pass']:
        print("✓ All gates PASS — Segment A trajectory is FEASIBLE with current specs.")
        sys.exit(0)
    else:
        print("✗ Some gates FAIL — Segment A trajectory needs design iteration.")
        sys.exit(1)
