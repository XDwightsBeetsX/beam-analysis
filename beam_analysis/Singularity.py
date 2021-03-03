"""
Used by Beam to make functions for shear/moment...
"""

import numpy as np

from .AppliedLoad import AppliedLoad
from .utils import *


class Singularity(object):
    def __init__(self, l, e, i, appliedLoads, boundaryConditions):
        self.L = l
        self.E = e
        self.I = i
        self.Terms = appliedLoads
        self.BoundaryConditions = boundaryConditions
    
    def evaluate(self, x_vals, analysis_type):
        """
        Evaluates the terms at a series of points,
        which are modified depending on analysis type
        """
        if analysis_type == ANGLE and len(self.BoundaryConditions) < 1:
            raise Exception(f"{ERROR_PREFIX_SINGULARITY} cannot evaluate angle with <1 boundary conditions")
        elif analysis_type == DEFLECTION and len(self.BoundaryConditions) < 2:
            raise Exception(f"{ERROR_PREFIX_SINGULARITY} cannot evaluate deflection with <2 boundary conditions")

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
            # Find boundary conditions
            for bc in self.BoundaryConditions:
                if bc.Bc_type == ANGLE:
                    angleBc = bc
            
            # Solve for angle boundary condition
            pre_c1_tot = 0
            for term in self.Terms:
                pre_c1_tot += term.evaluate(angleBc.Location, 2)
            c1 = angleBc.Bc_value - pre_c1_tot
            
            # Evaluate angles with c1
            for i in range(n):
                termTot = 0.0
                for term in self.Terms:
                    termVal = term.evaluate(x_vals[i], 2) + c1
                    termTot += termVal
                analysis_results[i] = (1 / (self.E * self.I)) * termTot
        elif analysis_type == DEFLECTION:
            # Find boundary conditions
            for bc in self.BoundaryConditions:
                if bc.Bc_type == ANGLE:
                    angleBc = bc
                elif bc.Bc_type == DEFLECTION:
                    defBc = bc
            
            # Solve for angle boundary condition
            pre_c1_tot = 0
            for term in self.Terms:
                pre_c1_tot += term.evaluate(angleBc.Location, 2)
            c1 = angleBc.Bc_value - pre_c1_tot
            # Add "applied load" 'angle_bc' to make linear term i.e. C1<x> + C2
            angleBcTerm = AppliedLoad(0, c1, ANGLE_BC)
            self.Terms.append(angleBcTerm)

            # Solve for deflection boundary condition
            pre_c2_tot = 0
            for term in self.Terms:
                pre_c2_tot += term.evaluate(angleBc.Location, 3)
            c2 = defBc.Bc_value - pre_c2_tot
            
            # Evaluate deflections with:  AppliedLoad(c1<x>) + c2
            for i in range(n):
                termTot = 0.0
                for term in self.Terms:
                    termTot += term.evaluate(x_vals[i], 3) + c2
                analysis_results[i] = (1 / (self.E * self.I)) * termTot
            
            # Remove linear term C1 from C1<x> + C2
            self.Terms.remove(angleBcTerm)
        else:
            raise Exception(f"{ERROR_PREFIX_SINGULARITY} invalid analysis type: '{analysis_type}'")
        
        return analysis_results
