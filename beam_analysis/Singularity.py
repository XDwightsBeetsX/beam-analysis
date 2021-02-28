"""
Used by Beam to make functions for shear/moment...
"""
from .utils import *

class Singularity(object):
    def __init__(self, length):
        self.L = length
        self.Components = []
    
    def addComponent(self, start, coefficient, power):
        if self.L < start or start < 0:
            raise Exception(f"{ERROR_PREFIX_SINGULARITY} invalid start bound: '{start}'")
        component = Component(start, coefficient, power)
        self.Components.append(component)
    
    def evaluate(self, point):
        pass


class Component(object):
    def __init__(self, start, coefficient, power):
        self.Start = start
        self.Coefficient = coefficient
        self.Power = power