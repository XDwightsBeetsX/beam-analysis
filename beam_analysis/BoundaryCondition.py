
from enum import Enum

class BoundaryCondition(object):
    
    def __init__(self, location, boundaryConditionType, boundaryConditionValue, plane):
        """
        `location` - the distance along the beam to the boundary condition

        `boundaryConditionType` - angle, deflection

        `boundaryConditionValue` - the value of the boundary condition, typically 0
        """
        self.Location = location
        self.BoundaryConditionType = boundaryConditionType
        self.BoundaryConditionValue = boundaryConditionValue


class BoundaryConditionTypes(Enum):
    ANGLE = 1
    DEFLECTION = 2
