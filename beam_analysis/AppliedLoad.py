"""
AppliedLoad class used in Beam and Singularity
"""

import numpy as np

from .utils import MOMENT, POINT_LOAD, DISTRIBUTED_LOAD


class AppliedLoad(object):
    """
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
        if origin == MOMENT:
            self.Power = -1
        elif origin == POINT_LOAD:
            self.Power = 0
        elif origin == DISTRIBUTED_LOAD:
            self.Power = 1
    
    def getString(self):
        s = f"{self.Coefficient}<x-{self.Start}>^{self.Power}"
        return s
    
    def evaluate(self, point, powerModifier):
        if point < self.Start:
            return 0
        elif (self.Power + powerModifier) < 0:
            return 0
        elif (self.Power + powerModifier) == 0:
            return self.Coefficient
        elif self.Coefficient == 0:
            return 0
        elif (self.Power + powerModifier) == 1:
            return self.Coefficient * (point - self.Start)
        else:
            effPower = self.Power + powerModifier
            return (self.Coefficient / np.math.factorial(effPower)) * (point - self.Start)**(effPower)
