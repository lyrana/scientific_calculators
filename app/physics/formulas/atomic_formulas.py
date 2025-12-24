"""
Atomic Physics Formulas

Formulas for atomic mass and related calculations.
"""

from ..constants import AMU_TO_KG


def calculate_mass_conversion(amu: float) -> dict:
    """
    Convert atomic mass units to kilograms.

    Args:
        amu: Mass in atomic mass units

    Returns:
        dict with:
            - mass_kg: Mass in kilograms
    """
    mass_kg = AMU_TO_KG * amu
    return {"mass_kg": mass_kg}
