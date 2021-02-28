"""
Used by Beam to make functions for shear/moment...
"""
from .utils import *

class Singularity(object):
    def __init__(self, length):
        self.L = length
        self.Terms = []
    
    def addTerm(self, start, coefficient, power):
        if self.L < start or start < 0:
            raise Exception(f"{ERROR_PREFIX_SINGULARITY} invalid start bound: '{start}'")
        term = Term(start, coefficient, power)
        self.Terms.append(term)
    
    def evaluate(self, point, powerIncrement):
        val = 0.0
        for term in self.Terms:
            val += term.evaluate(point, powerIncrement)
        return val


class Term(object):
    def __init__(self, start, coefficient, power):
        self.Start = start
        self.Coefficient = coefficient
        self.Power = power
    
    def evaluate(self, point, powerIncrement):
        if self.Start < point:
            return 0
        if self.Coefficient == 0:
            return 0
        if self.Power < 0:
            return 0
        return self.Coefficient * (point - self.Start)**(self.Power + powerIncrement)