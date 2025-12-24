"""
Pulsed Power Formulas

Formulas for transmission line impedance and power flux calculations.
"""

import math
from ..constants import C_MKS, EPSILON_0, MU_0, PI


def calculate_transmission_line_impedance(
    line_type: str,
    dimension1: float,
    dimension2: float,
    relative_permittivity: float = 1.0,
    relative_permeability: float = 1.0,
) -> dict:
    """
    Calculate transmission line characteristic impedance.

    Args:
        line_type: Either "coaxial" or "radial"
        dimension1: For coaxial: inner radius (cm); For radial: radius (cm)
        dimension2: For coaxial: outer radius (cm); For radial: width (cm)
        relative_permittivity: Relative permittivity (epsilon_r)
        relative_permeability: Relative permeability (mu_r)

    Returns:
        dict with:
            - impedance: Characteristic impedance (ohms)

    Raises:
        ValueError: If coaxial inner radius >= outer radius
    """
    # Calculate impedance factor
    imped_factor = math.sqrt(relative_permittivity / relative_permeability)

    if line_type == "coaxial":
        inner = dimension1
        outer = dimension2
        if inner >= outer:
            raise ValueError("The inner radius must be smaller than the outer radius.")
        ratio = outer / inner
        impedance = 60 * math.log(ratio) * imped_factor
    else:  # radial
        radius = dimension1
        width = dimension2
        impedance = (60 * width / radius) * imped_factor

    return {"impedance": impedance}


def calculate_power_flux(
    input_value: float,
    input_type: str,
) -> dict:
    """
    Calculate power flux (Poynting vector) relationships.

    Args:
        input_value: Either electric field (V/m) or Poynting flux (W/m^2)
        input_type: Either "electric_field" or "poynting_flux"

    Returns:
        dict with:
            - poynting_flux: Power density (W/m^2)
            - electric_field: Electric field amplitude (V/m)
            - magnetic_field: Magnetic field strength (T) - only for flux input
    """
    if input_type == "electric_field":
        E = input_value
        # P = epsilon_0 * c * E^2
        P = EPSILON_0 * C_MKS * E * E
        return {
            "poynting_flux": P,
            "electric_field": E,
        }
    else:  # poynting_flux
        P = input_value
        # E = sqrt(P / (epsilon_0 * c))
        E = math.sqrt(P / (EPSILON_0 * C_MKS))
        # H = E / 377 (impedance of free space)
        H = E / 377
        # B = mu_0 * H
        B = MU_0 * H
        return {
            "poynting_flux": P,
            "electric_field": E,
            "magnetic_field": B,
        }
