from enum import Enum


class BeamAnalysisTypes(Enum):
    """
    The assigned values here matter and are used in Singularity analysis
    """
    SHEAR = 1
    BENDING = 2
    ANGLE = 3
    DEFLECTION = 4
