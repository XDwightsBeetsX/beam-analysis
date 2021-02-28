"""
Contains useful information and constants for the project
- prefixes
- constants
"""


# ================================ #
# ========= PREFIXES ============= #
# ================================ #
ERROR_PREFIX = "[BEAM_ANALYSIS] -"
ERROR_PREFIX_BEAM = ERROR_PREFIX + " [BEAM] -"
ERROR_PREFIX_SINGULARITY = ERROR_PREFIX + " [SINGULARITY] -"


# ================================ #
# ========== CONSTANTS =========== #
# ================================ #
G = 9.80665  # m/s^2


# ================================ #
# ========= CONVERSIONS ========== #
# ================================ #
CONVERSION_LB_TO_KG = 2.20462262185
CONVERSION_FT_TO_M = 0.3048

CONVERSION_D_TO_SI = (CONVERSION_LB_TO_KG * G) / CONVERSION_FT_TO_M  # distributed load
CONVERSION_F_TO_SI = G / CONVERSION_LB_TO_KG  # point load
CONVERSION_M_TO_SI = CONVERSION_FT_TO_M * CONVERSION_LB_TO_KG  # moment