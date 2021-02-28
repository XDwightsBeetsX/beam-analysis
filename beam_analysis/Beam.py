"""
Primary file for beam_analysis
"""

import numpy as np
from matplotlib import pyplot as plt

from .utils import *
from .Singularity import Singularity


class Beam(object):
    """
    ForcesAndMoments Dict Key Codes:  
    PointLoad:          ['F,loc'] = mag  
    DistributedLoad:    ['D,start,stop'] = mag  
    AppliedMoment:      ['M,loc'] = mag
    """
    def __init__(self, e, i, l):
        self.E = e
        self.I = i
        self.L = l
        self.Singularity = Singularity(l)
        
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
        
        self.Singularity.addTerm(start, mag, -1)
        # Add counteracting distributed load if terminates before beam length
        if stop < self.L:
            self.Singularity.addTerm(stop, -mag, -1)
    
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
        self.Singularity.addTerm(loc, mag, 0)

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
        self.Singularity.addTerm(loc, mag, -1)
    
    def getAnalysis(self, n=10**3, include=["F", "M", "A", "D"]):
        """
        include=["F", "M", "A", "D"]  
            F - Forces  
            M - Moments  
            A - Angle  
            D - Deflection  
        """
        for analysis in include:
            if analysis not in ["F", "M", "A", "D"]:
                raise Exception(f"{ERROR_PREFIX_BEAM} invalid analysis request: '{analysis}'")
            if analysis == "F":
                shear = np.zeros(n)
            elif analysis == "M":
                moment = np.zeros(n)
            elif analysis == "A":
                angle = np.zeros(n)
            elif analysis == "D":
                deflection = np.zeros(n)

        for i in range(n):
            for analysis in include:
                if analysis == "F":
                    shear[i] = self.Singularity.evaluate(i, 0)
                if analysis == "M":
                    moment[i] = self.Singularity.evaluate(i, 1)
                if analysis == "A":
                    angle[i] = self.Singularity.evaluate(i, 2)
                if analysis == "D":
                    deflection[i] = self.Singularity.evaluate(i, 3)
        

        analysis_results = (shear, moment, angle, deflection)
        
        return analysis_results
    
    def showForcesAndMoments(self):
        for k, v in self.ForcesAndMoments.items():
            print(f"{k}: {v}")

    def showParams(self):
        print(f"E = {self.E:.4f}Pa")
        print(f"I = {self.I:.4f}m^4")
        print(f"L = {self.L:.4f}m")
        
    def analyze(self, n=1000, analysis_includes=["F", "M", "A", "D"]):
        """Plots deflections and reports max deflection"""       

        analysis = self.getAnalysis(include=analysis_includes)

        # Data collection
        for i in range(n):
            pt = x[i]
            s = self.getShear(pt)
            m = self.getMoment(pt)
            a = self.getAngle(pt)
            d = self.getDeflection(pt)

            shear[i] = s
            moment[i] = m
            angle[i] = a
            deflection[i] = d
            
            if abs(s) > abs(max_shear[1]):
                max_shear[0] = pt
                max_shear[1] = s
            if abs(m) > abs(max_moment[1]):
                max_moment[0] = pt
                max_moment[1] = m
            if abs(a) > abs(max_angle[1]):
                max_angle[0] = pt
                max_angle[1] = a
            if abs(d) > abs(max_deflection[1]):
                max_deflection[0] = pt
                max_deflection[1] = d
            
        
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
        print(f"Max shear:      {max_shear[1]:.4f} [N] @ {max_shear[0]:.4f}m")
        print(f"Max moment:     {max_moment[1]:.4f} [N-m] @ {max_moment[0]:.4f}m")
        print(f"Max angle:      {max_angle[1]:.4f} [rad] @ {max_angle[0]:.4f}m")
        print(f"Max deflection: {max_deflection[1]:.4f} [m] @ {max_deflection[0]:.4f}m\n")

        plt.show()
