
from enum import Enum


class AppliedLoadTypes(Enum):
    """
    The assigned values here matter and are used in Singularity analysis
    """
    DISTRIBUTED_LOAD = 1
    POINT_LOAD = 2
    MOMENT = 3


class BeamAnalysisTypes(Enum):
    """
    The assigned values here matter and are used in Singularity analysis
    """
    SHEAR = 1
    BENDING = 2
    ANGLE = 3
    DEFLECTION = 4


class BoundaryConditionTypes(Enum):
    ANGLE = 1
    DEFLECTION = 2
