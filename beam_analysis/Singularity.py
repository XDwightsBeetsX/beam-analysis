"""
Used by Beam to make functions for shear/moment...
"""

import numpy as np

from .AppliedLoad import AppliedLoad
from .utils import *


class Singularity(object):
    def __init__(self, l, e, i, appliedLoads):
        self.L = l
        self.E = e
        self.I = i
        self.Terms = appliedLoads
    
    def evaluate(self, x_vals, analysis_type):
        """
        Evaluates the terms at a series of points,
        which are modified depending on analysis type
        """
        n = len(x_vals)
        analysis_results = np.zeros(n)
        if analysis_type == SHEAR:
            for i in range(n):
                termTot = 0.0
                for term in self.Terms:
                    termTot += term.evaluate(x_vals[i], 0)
                analysis_results[i] = termTot
        elif analysis_type == MOMENT:
            for i in range(n):
                termTot = 0.0
                for term in self.Terms:
                    termTot += term.evaluate(x_vals[i], 1)
                analysis_results[i] = termTot
        elif analysis_type == ANGLE:
            for i in range(n):
                termTot = 0.0
                for term in self.Terms:
                    termTot += term.evaluate(x_vals[i], 2)
                analysis_results[i] = (1 / (self.E * self.I)) * termTot
        elif analysis_type == DEFLECTION:
            for i in range(n):
                termTot = 0.0
                for term in self.Terms:
                    termTot += term.evaluate(x_vals[i], 3)
                analysis_results[i] = (1 / (self.E * self.I)) * termTot
        else:
            raise Exception(f"{ERROR_PREFIX_SINGULARITY} invalid analysis type: '{analysis_type}'")
        
        return analysis_results
