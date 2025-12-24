"""
Material Properties Database

This module contains physical properties for various materials used in
scattering and beam physics calculations.
"""

from typing import Dict, Any

# Material properties dictionary
# Each material has:
#   - density: g/cm^3
#   - g_mole: atomic/molecular weight in g/mol
#   - z: atomic number (effective Z for compounds)
#   - name: display name

MATERIALS: Dict[str, Dict[str, Any]] = {
    "aluminum": {
        "density": 2.7,      # g/cm^3
        "g_mole": 27.0,      # g/mol
        "z": 13,             # atomic number
        "name": "Aluminum",
    },
    "beryllium": {
        "density": 1.85,     # g/cm^3
        "g_mole": 9.01,      # g/mol
        "z": 4,              # atomic number
        "name": "Beryllium",
    },
    "calcium": {
        "density": 2.0,      # g/cm^3 (actually carbon in original code)
        "g_mole": 12.0,      # g/mol
        "z": 6,              # atomic number
        "name": "Carbon",    # Note: labeled as Calcium in original but properties are Carbon
    },
    "iron": {
        "density": 7.87,     # g/cm^3
        "g_mole": 55.85,     # g/mol
        "z": 26,             # atomic number
        "name": "Iron",
    },
    "kapton": {
        "density": 1.42,     # g/cm^3
        "g_mole": 13.44,     # g/mol (effective)
        "z": 7,              # effective Z
        "name": "Kapton",
    },
    "nickel": {
        "density": 8.9,      # g/cm^3
        "g_mole": 58.69,     # g/mol
        "z": 28,             # atomic number
        "name": "Nickel",
    },
    "tantalum": {
        "density": 16.6,     # g/cm^3
        "g_mole": 180.95,    # g/mol
        "z": 73,             # atomic number
        "name": "Tantalum",
    },
    "titanium": {
        "density": 4.5,      # g/cm^3
        "g_mole": 47.88,     # g/mol
        "z": 23,             # atomic number
        "name": "Titanium",
    },
    "tungsten": {
        "density": 19.3,     # g/cm^3
        "g_mole": 183.85,    # g/mol
        "z": 74,             # atomic number
        "name": "Tungsten",
    },
}

# Ionization energies for various species (eV)
IONIZATION_ENERGIES: Dict[str, Dict[str, Any]] = {
    "Ar": {"energy": 15.8, "name": "Argon"},
    "Cs": {"energy": 3.9, "name": "Cesium"},
    "H": {"energy": 13.6, "name": "Hydrogen"},
    "H2": {"energy": 15.4, "name": "Molecular Hydrogen", "display": "H\u2082"},
    "He": {"energy": 24.6, "name": "Helium"},
    "Kr": {"energy": 14.0, "name": "Krypton"},
    "N2": {"energy": 15.6, "name": "Molecular Nitrogen", "display": "N\u2082"},
    "Ne": {"energy": 21.6, "name": "Neon"},
    "O2": {"energy": 12.1, "name": "Molecular Oxygen", "display": "O\u2082"},
    "SF6": {"energy": "13.42 - 15.9", "name": "Sulfur Hexafluoride", "display": "SF\u2086"},
    "TMAE": {"energy": 6.1, "name": "TMAE", "note": "Tetrakis Dimethylamine Ethylene, λ = 200nm"},
    "Xe": {"energy": 12.1, "name": "Xenon"},
}

# Cross-section image files
CROSS_SECTION_IMAGES = [
    {"id": "h2", "name": "Molecular Hydrogen", "file": "h2_2001.png"},
    {"id": "he", "name": "Helium", "file": "he2002.png"},
    {"id": "ar", "name": "Argon", "file": "ar2002.png"},
    {"id": "n2", "name": "Molecular Nitrogen", "file": "n22003.png"},
    {"id": "o2", "name": "Molecular Oxygen", "file": "ox2004.png"},
    {"id": "h2o", "name": "Water Vapor", "file": "h2o2004.png"},
    {"id": "cs", "name": "Cesium", "file": "cesium.png"},
    {"id": "hg", "name": "Mercury", "file": "hg2003.png"},
]


def get_material(name: str) -> Dict[str, Any]:
    """Get material properties by name (case-insensitive)."""
    return MATERIALS.get(name.lower(), MATERIALS["tungsten"])


def get_material_names() -> list:
    """Get list of available material names for dropdown."""
    return [mat["name"] for mat in MATERIALS.values()]


def get_material_keys() -> list:
    """Get list of material keys."""
    return list(MATERIALS.keys())
