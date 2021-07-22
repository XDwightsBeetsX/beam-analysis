
from enum import Enum


class Planes(Enum):
    XY = 1
    XZ = 2


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
    SHEAR = 0
    BENDING = 1
    ANGLE = 2
    DEFLECTION = 3


class BoundaryConditionTypes(Enum):
    ANGLE = 1
    DEFLECTION = 2
