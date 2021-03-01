"""
Used by Beam to make functions for shear/moment...
"""

import numpy as np

from .utils import *


class Singularity(object):
    def __init__(self, l, e, i):
        self.L = l
        self.E = e
        self.I = i
        self.Terms = []
    
    def addTerm(self, start, magnitude, origin):
        if self.L < start or start < 0:
            raise Exception(f"{ERROR_PREFIX_SINGULARITY} invalid start bound: '{start}'")
        term = Term(start, magnitude, origin)
        self.Terms.append(term)
    
    def getString(self):
        s = ""
        for term in self.Terms:
            ts = term.getString()
            if term.Coefficient >= 0:
                s += " + " + ts
            else:
                ts = ts[1:]
                s += " - " + ts
        return s
    
    def evaluate(self, point, analysis_type):
        """
        Evaluates all self.Terms at a point for an analysis type
        """
        termTot = 0.0
        for term in self.Terms:
            if analysis_type == SHEAR:
                termVal = term.evaluate(point, 0)
            elif analysis_type == MOMENT:
                termVal = term.evaluate(point, 1)
            elif analysis_type == ANGLE:
                termVal = (1 / (self.E * self.I)) * term.evaluate(point, 2)
            elif analysis_type == DEFLECTION:
                termVal = (1 / (self.E * self.I)) * term.evaluate(point, 3)
            else:
                raise Exception(f"{ERROR_PREFIX_SINGULARITY} invalid analysis type: '{analysis_type}'")
            termTot += termVal
        
        return termTot


class Term(object):
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
    
    def evaluate(self, point, powerIncrement):
        effectivePower = self.Power + powerIncrement
        if self.Start < point:
            return 0
        elif effectivePower < 0:
            return 0
        elif self.Coefficient == 0:
            return 0
        elif effectivePower == 0:
            return self.Coefficient
        elif effectivePower == 1:
            val = self.Coefficient * (point - self.Start)
            return val
        else:
            val = (self.Coefficient / np.math.factorial(effectivePower)) * (point - self.Start)**(effectivePower)
            return val
    
    def getString(self):
        s = f"{self.Coefficient}<x-{self.Start}>^{self.Power}"
        return s
