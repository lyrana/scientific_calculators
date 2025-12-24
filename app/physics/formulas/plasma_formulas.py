"""
Plasma Physics Formulas

Formulas for plasma parameter calculations.
All calculations use CGS units and results are in CGS units.
"""

import math
from ..constants import (
    C_CGS, PI, PLASMA_FREQ_COEFF, CYCLOTRON_FREQ_COEFF,
    CYCLOTRON_FREQ_HZ_COEFF, THERMAL_SPEED_COEFF, DEBYE_COEFF,
    ALFVEN_COEFF, NU_E_COEFF, NU_I_COEFF, SIGMA_COEFF, ETA_COEFF,
    LOSCHMIDT, P_STP_TORR, T_STP_K, TORR_TO_PA
)


def calculate_plasma_frequency(electron_density: float) -> dict:
    """
    Calculate electron plasma frequency.

    Args:
        electron_density: Electron density (cm^-3)

    Returns:
        dict with:
            - omega_pe: Plasma frequency (rad/s)
            - f_pe: Plasma frequency (Hz)
            - skin_depth: Collisionless skin depth (cm)
    """
    # omega_pe = 8978 * sqrt(n_e) * 2*pi
    f_pe = PLASMA_FREQ_COEFF * math.sqrt(electron_density)
    omega_pe = f_pe * 2 * PI

    # Collisionless skin depth c/omega_pe
    skin_depth = C_CGS / omega_pe

    return {
        "omega_pe": omega_pe,
        "f_pe": f_pe,
        "skin_depth": skin_depth,
    }


def calculate_cyclotron_frequency(magnetic_field: float) -> dict:
    """
    Calculate electron cyclotron frequency.

    Args:
        magnetic_field: Magnetic field (Gauss)

    Returns:
        dict with:
            - omega_ce: Cyclotron frequency (rad/s)
            - f_ce: Cyclotron frequency (Hz)
    """
    omega_ce = CYCLOTRON_FREQ_COEFF * magnetic_field
    f_ce = CYCLOTRON_FREQ_HZ_COEFF * magnetic_field

    return {
        "omega_ce": omega_ce,
        "f_ce": f_ce,
    }


def calculate_thermal_speed(temperature_ev: float) -> dict:
    """
    Calculate electron thermal speed.

    v_th = sqrt(T_eV / 511000) * c

    Args:
        temperature_ev: Electron temperature (eV)

    Returns:
        dict with:
            - thermal_speed: Electron thermal speed (cm/s)
    """
    speed = THERMAL_SPEED_COEFF * math.sqrt(temperature_ev)
    return {"thermal_speed": speed}


def calculate_debye_length(
    electron_density: float,
    temperature_ev: float,
) -> dict:
    """
    Calculate Debye length.

    lambda_D = 743.5 * sqrt(T_eV / n_e)

    Args:
        electron_density: Electron density (cm^-3)
        temperature_ev: Plasma temperature (eV)

    Returns:
        dict with:
            - debye_length: Debye length (cm)
    """
    debye = DEBYE_COEFF * math.sqrt(temperature_ev / electron_density)
    return {"debye_length": debye}


def calculate_alfven_speed(
    magnetic_field: float,
    electron_density: float,
    atomic_weight: float,
) -> dict:
    """
    Calculate Alfven speed.

    v_A = 2.2e11 * B / sqrt(n_e * A)

    Args:
        magnetic_field: Magnetic field (Gauss)
        electron_density: Electron density (cm^-3)
        atomic_weight: Ion atomic weight (amu)

    Returns:
        dict with:
            - alfven_speed: Alfven speed (cm/s)
    """
    speed = ALFVEN_COEFF * magnetic_field / (math.sqrt(electron_density) * math.sqrt(atomic_weight))
    return {"alfven_speed": speed}


def calculate_plasma_beta(
    magnetic_field: float,
    electron_density: float,
    temperature_ev: float,
) -> dict:
    """
    Calculate plasma beta (ratio of plasma pressure to magnetic pressure).

    beta = n * k * T / (B^2 / 8*pi)

    Args:
        magnetic_field: Magnetic field (Gauss)
        electron_density: Electron density (cm^-3)
        temperature_ev: Plasma temperature (eV)

    Returns:
        dict with:
            - beta: Plasma beta (electron pressure only)
    """
    # Magnetic pressure: B^2 / (8*pi)
    B_pressure = magnetic_field * magnetic_field / (8 * PI)

    # Electron pressure: n * 1.602e-12 * T_eV (converting eV to ergs)
    e_pressure = electron_density * 1.602e-12 * temperature_ev

    beta = e_pressure / B_pressure
    return {"beta": beta}


def _coulomb_log_ei(n: float, T_e: float, z: float, A: float, T_i: float) -> float:
    """
    Calculate electron-ion Coulomb logarithm.

    Different formulas apply depending on temperature regimes.
    """
    if 10 * z * z > T_e and T_e > T_i / (A * 1840):
        # Low temperature regime
        val = math.sqrt(n) * z * (T_e ** (-1.5))
        return 23 - math.log(val)
    elif T_e > 10 * z * z and 10 * z * z > T_i / (A * 1840):
        # Intermediate regime
        val = math.sqrt(n) * (T_e ** (-1))
        return 24 - math.log(val)
    elif T_i > T_e * (1840 * A / z):
        # High ion temperature regime
        val = math.sqrt(n) * (T_e ** (-1.5)) * z * z * (A ** (-1))
        return 30 - math.log(val)
    else:
        raise ValueError("These parameters result in a negative Coulomb logarithm!")


def _coulomb_log_ee(n: float, T_e: float) -> float:
    """Calculate electron-electron Coulomb logarithm."""
    if T_e <= 10:
        val = math.sqrt(n) * (T_e ** (-1.5))
        return 23 - math.log(val)
    else:
        val = math.sqrt(n) * (T_e ** (-1))
        return 24 - math.log(val)


def _coulomb_log_ii(n: float, z: float, T_i: float) -> float:
    """Calculate ion-ion Coulomb logarithm."""
    return 23.0 - math.log((z * z / T_i) * math.sqrt(2 * n * z / T_i))


def calculate_coulomb_rates(
    electron_density: float,
    electron_temp: float,
    ion_temp: float,
    atomic_weight: float,
    z: float,
) -> dict:
    """
    Calculate Coulomb collision rates and transport coefficients.

    Args:
        electron_density: Electron density (cm^-3)
        electron_temp: Electron temperature (eV)
        ion_temp: Ion temperature (eV)
        atomic_weight: Ion atomic weight (amu)
        z: Ion charge state

    Returns:
        dict with:
            - lambda_ei: Electron-ion Coulomb logarithm
            - lambda_ii: Ion-ion Coulomb logarithm
            - nu_e: Electron collision frequency (s^-1)
            - nu_i: Ion collision frequency (s^-1)
            - conductivity: Plasma conductivity ((ohm-cm)^-1)
            - resistivity: Plasma resistivity (ohm-cm)
    """
    # Coulomb logarithms
    lambda_ei = _coulomb_log_ei(electron_density, electron_temp, z, atomic_weight, ion_temp)
    lambda_ii = _coulomb_log_ii(electron_density, z, ion_temp)

    # Collision frequencies
    T_e32 = math.sqrt(electron_temp ** 3)
    nu_e = NU_E_COEFF * electron_density * z * lambda_ei / T_e32

    T_i32 = math.sqrt(ion_temp ** 3)
    nu_i = NU_I_COEFF * electron_density * lambda_ii / T_i32
    nu_i = nu_i * (z ** 3.0) / math.sqrt(atomic_weight)

    # Conductivity and resistivity
    sigma = SIGMA_COEFF * T_e32 / lambda_ei
    eta = 100.0 * ETA_COEFF / sigma

    return {
        "lambda_ei": lambda_ei,
        "lambda_ii": lambda_ii,
        "nu_e": nu_e,
        "nu_i": nu_i,
        "conductivity": sigma,
        "resistivity": eta,
    }


def calculate_neutral_density(
    pressure: float,
    pressure_units: str,
    temperature: float,
) -> dict:
    """
    Calculate neutral gas density from ideal gas law.

    n = 2.687e19 * (P/760) * (273/T)

    Args:
        pressure: Gas pressure
        pressure_units: Either "torr" or "Pa"
        temperature: Gas temperature (K)

    Returns:
        dict with:
            - neutral_density: Neutral density (cm^-3)
    """
    # Convert pressure to torr if needed
    if pressure_units == "Pa":
        p_torr = pressure / TORR_TO_PA
    else:
        p_torr = pressure

    # Ideal gas law calculation
    n = LOSCHMIDT * (p_torr / P_STP_TORR) * (T_STP_K / temperature)

    return {"neutral_density": n}
