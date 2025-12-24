"""
Physical Constants for Scientific Calculators

This module contains all physical constants used across the calculators.
Constants are organized by unit system (CGS vs MKS) and application area.
"""

import math

# =============================================================================
# FUNDAMENTAL CONSTANTS (MKS - SI Units)
# =============================================================================

# Speed of light in vacuum
C_MKS = 2.9979e8  # m/s

# Vacuum permittivity (electric constant)
EPSILON_0 = 8.8542e-12  # F/m (farads per meter)

# Vacuum permeability (magnetic constant)
MU_0 = 4e-7 * math.pi  # H/m (henries per meter)

# Impedance of free space
Z_0 = 377  # ohms (approximately sqrt(MU_0/EPSILON_0))

# =============================================================================
# FUNDAMENTAL CONSTANTS (CGS - Gaussian Units)
# =============================================================================

# Speed of light in vacuum
C_CGS = 3e10  # cm/s

# Planck's constant / 2pi
HBAR_CGS = 1.054e-27  # erg*s

# Planck's constant
H_CGS = 2 * math.pi * HBAR_CGS  # erg*s

# Elementary charge
E_CGS = 4.8e-10  # esu (statcoulombs)

# Electron mass
M_E_CGS = 9.11e-28  # grams

# =============================================================================
# ATOMIC AND PARTICLE CONSTANTS
# =============================================================================

# Avogadro's number
AVOGADRO = 6.022e23  # particles/mol

# Atomic mass unit to kg conversion
AMU_TO_KG = 1.66053886e-27  # kg

# Proton mass
PROTON_MASS_KG = 1.67262158e-27  # kg

# Electron mass
ELECTRON_MASS_KG = 9.10938188e-31  # kg

# Electron rest mass energy
ELECTRON_REST_MASS_MEV = 0.511  # MeV

# Electron rest mass energy in eV
ELECTRON_REST_MASS_EV = 511000  # eV

# =============================================================================
# PLASMA PHYSICS CONSTANTS (CGS)
# =============================================================================

# Electron plasma frequency coefficient
# omega_pe = 8978 * sqrt(n_e) where n_e is in cm^-3
PLASMA_FREQ_COEFF = 8978  # rad/s per sqrt(cm^-3)

# Electron cyclotron frequency coefficient
# omega_ce = 1.759e7 * B where B is in Gauss
CYCLOTRON_FREQ_COEFF = 1.759e7  # rad/s per Gauss
CYCLOTRON_FREQ_HZ_COEFF = 2.799e6  # Hz per Gauss

# Electron thermal speed coefficient
# v_th = 4.194e7 * sqrt(T_eV) where T is in eV
THERMAL_SPEED_COEFF = 4.194e7  # cm/s per sqrt(eV)

# Debye length coefficient
# lambda_D = 743.5 * sqrt(T_eV / n_e)
DEBYE_COEFF = 743.5  # cm

# Alfven speed coefficient
# v_A = 2.2e11 * B / sqrt(n_e * A)
ALFVEN_COEFF = 2.2e11  # cm/s

# Collision frequency coefficients
NU_E_COEFF = 2.9e-6  # electron-ion collision frequency coefficient
NU_I_COEFF = 4.8e-8  # ion-ion collision frequency coefficient

# Conductivity coefficient
SIGMA_COEFF = 8.74e13  # (ohm-cm)^-1

# Resistivity coefficient
ETA_COEFF = 9.0e9  # for eta calculation

# =============================================================================
# GAS CONSTANTS
# =============================================================================

# Loschmidt constant (number density at STP)
LOSCHMIDT = 2.687e19  # cm^-3 at 760 torr, 273 K

# Standard pressure
P_STP_TORR = 760  # torr
T_STP_K = 273  # K

# Pressure conversion
TORR_TO_PA = 133.32236  # Pa per torr

# =============================================================================
# MATHEMATICAL CONSTANTS
# =============================================================================

PI = math.pi
EULER_E = 2.71828
EULER_GAMMA = 1.7811  # Euler-Mascheroni constant exponential

# =============================================================================
# UNIT CONVERSION FACTORS
# =============================================================================

# Length
MIL_TO_CM = 2.54 / 1000.0  # cm per mil (1 mil = 0.001 inch)
MM_TO_CM = 0.1  # cm per mm
M_TO_CM = 100.0  # cm per m

# Energy
EV_TO_ERG = 1.602e-12  # erg per eV
