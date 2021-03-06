"""
AppliedLoad class used in Beam and Singularity
"""

import numpy as np

from .utils import MOMENT, POINT_LOAD, DISTRIBUTED_LOAD, ANGLE_BC


class AppliedLoad(object):
    """
    Effectively a Singularity Function term.  
    Stores information about an applied load:
    - Start  
    - Coefficient (Magnitude)  
    - Origin  
    - Power (Determined from Origin)
    """
    def __init__(self, start, coefficient, origin):
        self.Start = start
        self.Coefficient = coefficient
        self.Origin = origin
        if origin == ANGLE_BC:
            self.Power = -2
        elif origin == MOMENT:
            self.Power = -1
        elif origin == POINT_LOAD:
            self.Power = 0
        elif origin == DISTRIBUTED_LOAD:
            self.Power = 1
    
    def getString(self, powerModifier=0):
        effPower = self.Power + powerModifier
        if effPower < 0:
            return "0"
        elif effPower == 0:
            return f"{self.Coefficient}"
        elif effPower == 1:
            return f"{self.Coefficient}<x-{self.Start}>"
        else:
            return f"({self.Coefficient}/{np.math.factorial(effPower)})<x-{self.Start}>^{effPower}"
    
    def evaluate(self, point, powerModifier):
        if point < self.Start:
            return 0
        else:
            effPower = self.Power + powerModifier
            if effPower < 0:
                return 0
            elif effPower == 0:
                return self.Coefficient
            elif effPower == 1:
                return self.Coefficient * (point - self.Start)
            else:
                return (self.Coefficient / np.math.factorial(effPower)) * (point - self.Start)**(effPower)
