"""
Electromagnetic Formulas

Formulas for light wave propagation and skin depth calculations.
All calculations use MKS (SI) units unless otherwise noted.
"""

import math
from ..constants import C_MKS, MU_0, PI


def calculate_light_waves(
    input_value: float,
    input_type: str,
    relative_permittivity: float = 1.0,
    relative_permeability: float = 1.0,
) -> dict:
    """
    Calculate light wave properties in a medium.

    Args:
        input_value: Either wavelength (m or cm) or frequency (Hz)
        input_type: One of "wavelength_m", "wavelength_cm", or "frequency"
        relative_permittivity: Relative permittivity (epsilon_r)
        relative_permeability: Relative permeability (mu_r)

    Returns:
        dict with:
            - light_speed_m: Speed of light in medium (m/s)
            - light_speed_cm: Speed of light in medium (cm/s)
            - frequency: Frequency (Hz)
            - omega: Angular frequency (rad/s)
            - wavelength: Wavelength (m)
            - wavenumber: Wavenumber (1/m)
    """
    # Calculate light speed in medium
    n = math.sqrt(relative_permittivity * relative_permeability)
    v_light = C_MKS / n
    v_light_cm = v_light * 100.0

    result = {
        "light_speed_m": v_light,
        "light_speed_cm": v_light_cm,
    }

    if input_type == "wavelength_m":
        wavelength = input_value
        frequency = v_light / wavelength
        omega = frequency * 2.0 * PI
        wavenumber = 2.0 * PI / wavelength
        result.update({
            "frequency": frequency,
            "omega": omega,
            "wavelength": wavelength,
            "wavenumber": wavenumber,
        })

    elif input_type == "wavelength_cm":
        wavelength_cm = input_value
        wavelength = wavelength_cm / 100.0
        frequency = v_light / wavelength
        omega = frequency * 2.0 * PI
        wavenumber = 2.0 * PI / wavelength
        result.update({
            "frequency": frequency,
            "omega": omega,
            "wavelength": wavelength,
            "wavenumber": wavenumber,
        })

    else:  # frequency
        frequency = input_value
        omega = frequency * 2.0 * PI
        wavelength = v_light / frequency
        wavenumber = 2.0 * PI / wavelength
        result.update({
            "frequency": frequency,
            "omega": omega,
            "wavelength": wavelength,
            "wavenumber": wavenumber,
        })

    return result


def calculate_skin_depth(
    input_value: float,
    input_type: str,
    relative_permeability: float,
    conductivity: float,
) -> dict:
    """
    Calculate skin depth for electromagnetic waves in a conductor.

    Skin depth formula: delta = sqrt(2 / (mu * sigma * omega))

    Args:
        input_value: Either skin depth (m or cm) or frequency (Hz)
        input_type: One of "depth_m", "depth_cm", or "frequency"
        relative_permeability: Relative permeability (mu_r)
        conductivity: Electrical conductivity (S/m)

    Returns:
        dict with:
            - depth_m: Skin depth (m)
            - depth_cm: Skin depth (cm)
            - frequency: Frequency (Hz)
            - omega: Angular frequency (rad/s)
    """
    mu = relative_permeability * MU_0

    if input_type == "depth_m":
        depth = input_value
        # omega = 2 / (mu * sigma * delta^2)
        omega = 2.0 / (mu * conductivity * depth * depth)
        frequency = omega / (2.0 * PI)
        return {
            "depth_m": depth,
            "depth_cm": depth * 100.0,
            "frequency": frequency,
            "omega": omega,
        }

    elif input_type == "depth_cm":
        depth = input_value * 0.01  # Convert to meters
        omega = 2.0 / (mu * conductivity * depth * depth)
        frequency = omega / (2.0 * PI)
        return {
            "depth_m": depth,
            "depth_cm": depth * 100.0,
            "frequency": frequency,
            "omega": omega,
        }

    else:  # frequency
        frequency = input_value
        omega = frequency * 2.0 * PI
        # delta = sqrt(2 / (mu * sigma * omega))
        depth = math.sqrt(2.0 / (mu * conductivity * omega))
        return {
            "depth_m": depth,
            "depth_cm": depth * 100.0,
            "frequency": frequency,
            "omega": omega,
        }
