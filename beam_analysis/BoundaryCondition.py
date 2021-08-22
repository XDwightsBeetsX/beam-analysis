from enum import Enum


class BoundaryConditionTypes(Enum):
    ANGLE = 1
    DEFLECTION = 2


class BoundaryCondition(object):
    def __init__(self, location, type, value):
        """
        `location` - the distance along the beam to the boundary condition

        `type` - angle, deflection

        `value` - the value of the boundary condition, typically 0
        """
        self.Location = location
        self.Type = type
        self.Value = value
