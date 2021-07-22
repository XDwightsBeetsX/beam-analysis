
from beam_analysis.Enums import BoundaryConditionTypes


class BoundaryCondition(object):
    def __init__(self, location, boundaryConditionType, boundaryConditionValue):
        """
        `location` - the distance along the beam to the boundary condition

        `boundaryConditionType` - angle, deflection

        `boundaryConditionValue` - the value of the boundary condition, typically 0
        """
        self.Location = location
        self.BoundaryConditionType = boundaryConditionType
        self.BoundaryConditionValue = boundaryConditionValue
