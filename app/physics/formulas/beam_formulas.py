"""
Beam Physics Formulas

Formulas for particle beam calculations including Moliere scattering,
emittance, and beam breakup instability.

All calculations use CGS units unless otherwise noted.
"""

import math
from ..constants import (
    AVOGADRO, PI, E_CGS, M_E_CGS, C_CGS, HBAR_CGS,
    MIL_TO_CM, MM_TO_CM, ELECTRON_REST_MASS_EV, EULER_E, EULER_GAMMA
)
from ..materials import get_material


def _calculate_b_factor(n_collision: float, max_iterations: int = 10) -> float:
    """
    Iteratively calculate the Moliere B-factor.

    Args:
        n_collision: Number of collisions
        max_iterations: Maximum iterations for convergence

    Returns:
        B-factor for Moliere scattering
    """
    tmp_log = math.log(n_collision * EULER_E / (EULER_GAMMA * EULER_GAMMA))
    B = tmp_log
    for _ in range(max_iterations):
        B = tmp_log + math.log(B)
    return B


def calculate_moliere_scattering(
    thickness: float,
    thickness_units: str,
    element: str,
    energy_mev: float,
) -> dict:
    """
    Calculate Moliere multiple scattering parameters.

    Args:
        thickness: Foil thickness
        thickness_units: Either "mil" or "mm"
        element: Material name (e.g., "aluminum", "tungsten")
        energy_mev: Beam energy in MeV

    Returns:
        dict with:
            - thermal_momentum: Thermal momentum (gamma*beta units)
            - n_collisions: Number of collisions
            - theta_rms: RMS scattering angle (radians)
            - element_name: Display name of the element

    Raises:
        ValueError: If foil is too thin for the model
    """
    # Get material properties
    mat = get_material(element)
    density = mat["density"]
    gmole = mat["g_mole"]
    z = mat["z"]
    element_name = mat["name"]

    # Relativistic parameters
    gamma = energy_mev / 0.511 + 1
    beta = math.sqrt(1.0 - 1.0 / (gamma * gamma))

    # Bohr radius
    a0 = (HBAR_CGS / E_CGS) ** 2 / M_E_CGS

    # Convert thickness to cm
    if thickness_units == "mil":
        t = MIL_TO_CM * thickness
    else:  # mm
        t = MM_TO_CM * thickness

    # Atomic density
    atoms_cc = AVOGADRO * density / gmole

    # Calculate alpha squared (scattering cross-section factor)
    factor = E_CGS * E_CGS / (M_E_CGS * beta * beta * gamma * C_CGS * C_CGS)
    alpha_sq = 4.0 * PI * z * (z + 1) * factor * factor

    # Minimum scattering angle
    th_min = HBAR_CGS / (gamma * beta * M_E_CGS * C_CGS * a0 * (z ** (-1.0/3.0)))

    # Characteristic angle
    theta_c = math.sqrt(alpha_sq * t * atoms_cc)

    # Number of collisions
    n_collision = theta_c * theta_c / (1.13 * th_min * th_min)

    # Check validity
    log_val = math.log(theta_c / th_min)
    if log_val < 1:
        raise ValueError("The foil is too thin for this model to work.")

    # Calculate B-factor
    B = _calculate_b_factor(n_collision)

    # Moliere calculation
    theta_sq_mol = alpha_sq * atoms_cc * t * B
    theta_mol = math.sqrt(theta_sq_mol)

    # Thermal momentum
    gb_theta = gamma * beta * theta_mol
    p_th = 0.7071 * gb_theta

    return {
        "thermal_momentum": p_th,
        "n_collisions": n_collision,
        "theta_rms": theta_mol,
        "element_name": element_name,
    }


def calculate_emittance(
    radius: float,
    value: float,
    value_type: str,
) -> dict:
    """
    Calculate transverse beam emittance.

    Args:
        radius: Beam radius (cm)
        value: Either temperature (eV) or angle (radians)
        value_type: Either "ev" or "radians"

    Returns:
        dict with:
            - emittance: Transverse emittance (cm-rad)
            - angle: Divergence angle (radians)
            - temperature: Temperature (eV)
    """
    if value_type == "ev":
        temperature = value
        # theta = sqrt(T_eV / 511000)
        angle = math.sqrt(temperature / ELECTRON_REST_MASS_EV)
    else:  # radians
        angle = value
        # T = theta^2 * 511000
        temperature = angle * angle * ELECTRON_REST_MASS_EV

    # Emittance = 2 * radius * angle
    emittance = 2.0 * radius * angle

    return {
        "emittance": emittance,
        "angle": angle,
        "temperature": temperature,
    }


def calculate_beam_breakup(
    pulse_width_ns: float,
    frequency_mhz: float,
    b_field: float,
    current: float,
    n_gaps: float,
    impedance: float,
    q_factor: float,
) -> dict:
    """
    Calculate beam breakup (BBU) instability parameters.

    Args:
        pulse_width_ns: Pulse width (nanoseconds)
        frequency_mhz: Cavity frequency (MHz)
        b_field: Magnetic field (for focusing)
        current: Beam current
        n_gaps: Number of gaps
        impedance: Transverse impedance (Z)
        q_factor: Quality factor (Q)

    Returns:
        dict with:
            - time_max_growth: Time to maximum growth (ns)
            - damped_response: Damped response
            - delta: Delta function
            - resonant_response: Resonant response (if T/t >= 10)
    """
    T = pulse_width_ns / 1e9  # Convert to seconds
    F = frequency_mhz * 1e6  # Convert to Hz
    omega = 2 * PI * F

    alpha = omega / (2 * q_factor)
    r = n_gaps * current * impedance / (300 * b_field)
    t = 2 * r * q_factor / omega
    P = 2 * omega * T * n_gaps * current * impedance / (300 * b_field * q_factor)
    P = math.sqrt(P)

    result = {
        "time_max_growth": t * 1e9,  # Convert back to ns
    }

    if T >= t:
        # Greater than or equal to t
        denom = 4 * PI * r
        denom = math.sqrt(denom)
        damped = 0.5 * (math.exp(r) / denom)
        delta = damped / q_factor

        result["damped_response"] = damped
        result["delta"] = delta

        if T / t >= 10:
            res = 0.5 * math.exp(r)
            result["resonant_response"] = res
    else:
        # Less than t
        denom = 2 * PI * P
        denom = math.sqrt(denom)
        damped = 0.5 * (math.exp(P - alpha * T) / denom)
        delta = (damped / q_factor) * math.sqrt(t / T)

        result["damped_response"] = damped
        result["delta"] = delta

    return result
