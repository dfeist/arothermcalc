import math

# ────────────────────────────────────────────────────────────────
# Helper tables (distilled from the factory data you provided)
# ────────────────────────────────────────────────────────────────
def cond_offset(flow_t):
    """ΔT between mean water temp and refrigerant saturation (condenser)."""
    if flow_t <= 37:           # W30-/35-runs
        return 3.0             # K
    elif flow_t <= 52:         # W40-/45-runs
        return 4.0
    else:                      # ≥55 °C (DHW)
        return 5.0

def evap_offset(out_t):
    """ΔT between outdoor air and refrigerant saturation (evaporator)."""
    if out_t >= 5:             # mild
        return 5.0
    elif out_t >= 0:
        return 6.0
    elif out_t >= -5:
        return 7.0
    else:                      # ≤ -5 °C
        return 8.0

def eta_carnot(out_t, flow_t):
    """Whole-unit Carnot efficiency (Heat-pump factor)."""
    if out_t >= 5:
        base = 0.48
    elif out_t >= 0:
        base = 0.47
    elif out_t >= -5:
        base = 0.45
    else:
        base = 0.44

    # small penalty for hotter condenser water
    if flow_t >= 50:
        base -= 0.03
    elif flow_t >= 40:
        base -= 0.02
    return round(base, 3)

# ────────────────────────────────────────────────────────────────
# Main calculator
# ────────────────────────────────────────────────────────────────
def arotherm_cop(outdoor_c, flow_c, return_c):
    """Return dictionary with Carnot & real COP for the aroTHERM plus 7 kW."""
    t_cond_sat_k = (flow_c + return_c)/2 + cond_offset(flow_c) + 273.15
    t_evap_sat_k = outdoor_c - evap_offset(outdoor_c) + 273.15

    cop_carnot = t_cond_sat_k / (t_cond_sat_k - t_evap_sat_k)
    eta        = eta_carnot(outdoor_c, flow_c)
    cop_real   = eta * cop_carnot

    return {
        "Outdoor °C": outdoor_c,
        "Flow °C": flow_c,
        "Return °C": return_c,
        "ΔT_cond K": cond_offset(flow_c),
        "ΔT_evap K": evap_offset(outdoor_c),
        "ηCarnot":   eta,
        "Carnot COP": round(cop_carnot, 2),
        "Expected COP": round(cop_real, 2),
    }

# ── quick demo ──────────────────────────────────────────────────
print(arotherm_cop(10, 30, 25))   # mild weather space-heating
print(arotherm_cop( 0, 35, 30))   # freezing-point day
print(arotherm_cop(-3, 45, 40))   # colder, higher flow
print(arotherm_cop(10, 55, 48))   # DHW lift to 55 °C
