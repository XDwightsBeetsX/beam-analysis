from enum import Enum


class Units(Enum):
    Shear = 1
    Bending = 2
    Angle = 3
    Deflection = 4


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


class CrossSectionTypes(Enum):
    RECT = 1
    CIRC = 2
    I = 3  # TODO
