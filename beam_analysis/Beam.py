"""
Primary file for beam_analysis
"""

import numpy as np
from matplotlib import pyplot as plt

from .Singularity import Singularity
from .BoundaryCondition import BoundaryCondition
from .AppliedLoad import AppliedLoad
from .PointValuePair import PointValuePair
from .utils import *


class Beam(object):
    """
    Has material properties E, I, L as well as a Singularity function for the beam
    """
    def __init__(self, l, e, i):
        self.L = l
        self.E = e
        self.I = i
        self.AppliedLoads = []
        self.BoundaryConditions = []
        self.Singularity = None
    
    def showParams(self):
        print(f"E = {str(self.E)}Pa")
        print(f"I = {str(self.I)}m^4")
        print(f"L = {str(self.L)}m")
    
    def showAppliedLoads(self):
        s = ""
        for i in range(len(self.AppliedLoads)):
            term = self.AppliedLoads[i]
            ts = term.getString()
            if i == 0:
                s += ts
            elif term.Coefficient >= 0:
                s += " + " + ts
            else:
                ts = ts[1:]
                s += " - " + ts
        print(s)
    
    def addAppliedMoment(self, loc, mag, units="N-m"):
        """
        CC+  
        Conversion from 'lb-ft' or 'lbf-ft' to 'N-m'
        """
        magNM = mag
        if units != "N-m":
            if units == "lb-ft" or units == "lbf-ft":
                magNM *= CONVERSION_M_TO_SI
            else:
                raise Exception(f"{ERROR_PREFIX_BEAM} invalid units: '{units}'")
        self.AppliedLoads.append(AppliedLoad(loc, mag, MOMENT))
    
    def addPointLoad(self, loc, mag, units="N"):
        """
        Upward+  
        Conversion from 'lb' or 'lbf' to 'N'
        """
        magN = mag
        if units != "N":
            if units == "lb" or units == "lbf":
                magN *= CONVERSION_F_TO_SI
            else:
                raise Exception(f"{ERROR_PREFIX_BEAM} invalid units: '{units}'")
        self.AppliedLoads.append(AppliedLoad(loc, mag, POINT_LOAD))
    
    def addDistributedLoad(self, start, stop, mag, units="N/m"):
        """
        Beams do not enable gravity by default  
        Conversion from 'lb/ft' or 'lbf/ft' to 'N/m'
        """
        magNpM = mag
        if units != "N/m":
            if units == "lb/ft" or units == "lbf/ft":
                magNpM *= CONVERSION_D_TO_SI
            else:
                raise Exception(f"{ERROR_PREFIX_BEAM} invalid units: '{units}'")
        if stop < start:
            raise Exception(f"{ERROR_PREFIX_BEAM} invalid start/stop: '{start}/{stop}'")
        
        # Add counteracting distributed load if terminates before beam length
        if stop < self.L:
            self.AppliedLoads.append(AppliedLoad(stop, -mag, DISTRIBUTED_LOAD))
        self.AppliedLoads.append(AppliedLoad(start, mag, DISTRIBUTED_LOAD))
    
    def addBoundaryCondition(self, loc, bc_type=DEFLECTION, bc_value=0.0):
        """
        Beams require 2x BCs to analyze  
        bc_type can be "angle" or "deflection"  
        bc_value is typically 0.0
        """
        bc = BoundaryCondition(loc, bc_type, bc_value)
        self.BoundaryConditions.append(bc)

    def getAnalysis(self, n=10**3):
        """
        Returns tuple of analysis, all with len=n:  
            x       [0, L]  
            beam    0s  
            shear  
            moment  
            angle  
            deflection
        """
        self.Singularity = Singularity(self.L, self.E, self.I, self.AppliedLoads)

        x_vals = np.linspace(0, self.L, num=n)
        beam = np.zeros(n)
        shear = self.Singularity.evaluate(x_vals, SHEAR)
        moment = self.Singularity.evaluate(x_vals, MOMENT)
        angle = self.Singularity.evaluate(x_vals, ANGLE)
        deflection = self.Singularity.evaluate(x_vals, DEFLECTION)

        analysis_results = (x_vals, beam, shear, moment, angle, deflection)
        return analysis_results
        
    def analyze(self):
        """Plots deflections and reports max values from analysis"""       

        # if len(self.BoundaryConditions) < 2:
        #     raise Exception(f"{ERROR_PREFIX_BEAM} cannot run analysis without 2 boundary conditions")

        analysis = self.getAnalysis()
        x = analysis[0]
        beam = analysis[1]
        shear = analysis[2]
        moment = analysis[3]
        angle = analysis[4]
        deflection = analysis[5]

        print(shear)

        # Get maximum values
        max_shear = PointValuePair(0, 0.0, '[N]')
        max_moment = PointValuePair(0, 0.0, '[N-m]')
        max_angle = PointValuePair(0, 0.0, '[rad]')
        max_deflection = PointValuePair(0, 0.0, '[m]')
        for i in range(len(x)):
            if abs(shear[i]) > abs(max_shear.Value):
                max_shear.Value = shear[i]
                max_shear.Point = x[i]
            if abs(moment[i]) > abs(max_moment.Value):
                max_moment.Value = moment[i]
                max_moment.Point = x[i]
            if abs(angle[i]) > abs(max_angle.Value):
                max_angle.Value = angle[i]
                max_angle.Point = x[i]
            if abs(deflection[i]) > abs(max_deflection.Value):
                max_deflection.Value = deflection[i]
                max_deflection.Point = x[i]
        
        # Plotting
        fig, ax = plt.subplots(2, 2, sharex="all")

        xlabel = f"length (m)"
        t1 = f"Shear (N)"
        ax[0,0].plot(x, beam, '--k')
        ax[0,0].plot(x, shear, '-b', label=t1)
        ax[0,0].set(title=t1)

        t2 = f"Moment (N-m)"
        ax[1,0].plot(x, beam, '--k')
        ax[1,0].plot(x, moment, '-r', label=t2)
        ax[1,0].set(xlabel=xlabel, title=t2)

        t3 = f"Angle (rad)"
        ax[0,1].plot(x, beam, '--k')
        ax[0,1].plot(x, angle, '-y', label=t3)
        ax[0,1].set(title=t3)

        t4 = f"Deflection (m)"
        ax[1,1].plot(x, beam, '--k')
        ax[1,1].plot(x, deflection, '-g')
        ax[1,1].set(xlabel=xlabel, title=t4)

        fig.tight_layout()

        # Report
        print(f"\nREPORT:")
        print(f"Max shear:      {max_shear.getString()}")
        print(f"Max moment:     {max_moment.getString()}")
        print(f"Max angle:      {max_angle.getString()}")
        print(f"Max deflection: {max_deflection.getString()}")
        print()

        plt.show()
