"""
Used by Beam to make functions for shear/moment...
"""

import numpy as np

from .AppliedLoad import AppliedLoad
from .utils import *


class Singularity(object):
    def __init__(self, l, e, i, appliedLoads=[], boundaryConditions=[]):
        self.L = l
        self.E = e
        self.I = i
        self.Terms = appliedLoads
        self.BoundaryConditions = boundaryConditions
    
    def getAnalysis(self, x_vals, analysis_type, showLog=True):
        """
        Evaluates the terms at a series of points,
        which are modified depending on analysis type
        """
        if analysis_type == ANGLE and len(self.BoundaryConditions) < 1:
            raise Exception(f"{PREFIX_SINGULARITY} cannot evaluate angle with <1 boundary conditions")
        elif analysis_type == DEFLECTION and len(self.BoundaryConditions) < 2:
            raise Exception(f"{PREFIX_SINGULARITY} cannot evaluate deflection with <2 boundary conditions")

        n = len(x_vals)
        analysis_results = np.zeros(n)
        if analysis_type == SHEAR:
            if showLog:
                print(f"{PREFIX_SINGULARITY} running shear analysis: {self.getString()}")
            for i in range(n):
                analysis_results[i] = self.evaluate(x_vals[i], 0)
        elif analysis_type == MOMENT:
            if showLog:
                print(f"{PREFIX_SINGULARITY} running moment analysis: {self.getString(powerModifier=1)}")
            for i in range(n):
                analysis_results[i] = 1.0 * self.evaluate(x_vals[i], 1)
        elif analysis_type == ANGLE:
            if showLog:
                print(f"{PREFIX_SINGULARITY} running angle analysis: {self.getString(powerModifier=2)}")
            # Find boundary conditions
            for bc in self.BoundaryConditions:
                if bc.Bc_type == ANGLE:
                    angleBc = bc
            
            # Solve for angle boundary condition
            pre_c1_tot = self.evaluate(angleBc.Location, 2)
            c1 = angleBc.Bc_value - pre_c1_tot
            if showLog:
                print(f"{PREFIX_SINGULARITY} angle c1 found: {c1}")
            
            # Evaluate angles with c1
            for i in range(n):
                val = self.evaluate(x_vals[i], 2) + c1
                analysis_results[i] = (1 / (self.E * self.I)) * val
        elif analysis_type == DEFLECTION:
            if showLog:
                print(f"{PREFIX_SINGULARITY} running deflection analysis: {self.getString(powerModifier=3)}")
            # Find boundary conditions
            for bc in self.BoundaryConditions:
                if bc.Bc_type == ANGLE:
                    angleBc = bc
                elif bc.Bc_type == DEFLECTION:
                    defBc = bc
            
            # Solve for angle boundary condition
            pre_c1_tot = self.evaluate(angleBc.Location, 2)
            c1 = angleBc.Bc_value - pre_c1_tot
            if showLog:
                print(f"{PREFIX_SINGULARITY} deflection c1 found: {c1}")
            
            # Add "applied load" 'angle_bc' to make linear term i.e. C1<x> + C2
            angleBcTerm = AppliedLoad(0, c1, ANGLE_BC)
            self.Terms.append(angleBcTerm)

            # Solve for deflection boundary condition
            pre_c2_tot = self.evaluate(defBc.Location, 3)
            c2 = defBc.Bc_value - pre_c2_tot
            if showLog:
                print(f"{PREFIX_SINGULARITY} deflection c2 found: {c2}")
            
            # Evaluate deflections with:  AppliedLoad(c1<x>) + c2
            for i in range(n):
                termTot = self.evaluate(x_vals[i], 3) + c2
                analysis_results[i] = (1 / (self.E * self.I)) * termTot
            
            # Remove linear term C1 from C1<x> + C2
            self.Terms.remove(angleBcTerm)
        else:
            raise Exception(f"{PREFIX_SINGULARITY} invalid analysis type: '{analysis_type}'")
        
        return analysis_results

    def evaluate(self, point, powerModifier):
        termTot = 0.0
        for term in self.Terms:
            termTot += term.evaluate(point, powerModifier)
        
        return termTot
    
    def getString(self, powerModifier=0):
        s = ""
        for i, term in enumerate(sorted(self.Terms, key=lambda t: t.Start)):
            ts = term.getString(powerModifier=powerModifier)
            if i == 0:
                s += ts
            else:
                s += " + " + ts
        
        return s
