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
        
        self.Singularity.addComponent(start, mag, -1)
        # Add counteracting distributed load if terminates before beam length
        if stop < self.L:
            self.Singularity.addComponent(stop, -mag, -1)
    
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
        self.Singularity.addComponent(loc, mag, 0)

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
        self.Singularity.addComponent(loc, mag, -1)
    
    def getShear(self, x):
        """
        Returns the shear in the beam at a point x.
        
        Forces:             v  
        Distributed Loads:  v * x  
        Moments:            0  
        """
        s = 0
        for k, v in self.ForcesAndMoments.items():
            # pull type, loc, and mags from any applied loads
            app = k.split(',')

            # type of load [F, D, M]
            ty = app[0]
            start = float(app[1])
            if ty == 'F':
                if start <= x:
                    # apply load
                    s += v
            elif ty == 'D':
                end = float(app[2])
                if start <= x and x < end:
                    # apply load
                    eff = x - start
                    s += v * eff
            elif ty == 'M':
                continue
            else:
                raise Exception(f"{ERROR_PREFIX} invalid force/moment key: '{k}'")

        return s
    
    def getMoment(self, x):
        """
        Returns the moment in the beam at a point x.
        
        Forces:             v * x  
        Distributed Loads:  (1/2) * v * x**2  
        Moments:            v  
        """
        m = 0
        for k, v in self.ForcesAndMoments.items():
            # pull type, loc, and mags from any applied loads
            app = k.split(',')

            # type of load [F, D, M]
            ty = app[0]
            start = float(app[1])
            if ty == 'F':
                if start <= x:
                    # apply load
                    eff = x - start
                    m += v * eff
            elif ty == 'D':
                end = float(app[2])
                if start <= x and x < end:
                    # apply load
                    eff = x - start
                    m += (1/2) * v * eff**2
            elif ty == 'M':
                if start <= x:
                    # apply load
                    m += v
            else:
                raise Exception(f"{ERROR_PREFIX} invalid force/moment key: '{k}'")

        return m
    
    def getAngle(self, x):
        """
        Returns the angle in the beam at a point x.
        
        Forces:             (1/2) * v * x**2  
        Distributed Loads:  (1/6) * v * x**3  
        Moments:            v * x
        """
        ang = 0
        for k, v in self.ForcesAndMoments.items():
            # pull type, loc, and mags from any applied loads
            app = k.split(',')

            # type of load [F, D, M]
            ty = app[0]
            start = float(app[1])
            if ty == 'F':
                if start <= x:
                    # apply load
                    eff = x - start
                    ang += (1/2) * v * eff**2
            elif ty == 'D':
                end = float(app[2])
                if start <= x and x < end:
                    # apply load
                    eff = x - start
                    ang += (1/6) * v * eff**3
            elif ty == 'M':
                if start <= x:
                    # apply load
                    eff = x - start
                    ang += v * eff
            else:
                raise Exception(f"{ERROR_PREFIX} invalid force/moment key: '{k}'")
        return (1/(self.E * self.I)) * ang
    
    def getDeflection(self, x):
        """
        Returns the deflection in the beam at a point x.
        
        Forces:             (1/6) * v * x**3  
        Distributed Loads:  (1/24) * v * x**4  
        Moments:            (1/6) * v * x**2
        """
        d = 0
        for k, v in self.ForcesAndMoments.items():
            # pull type, loc, and mags from any applied loads
            app = k.split(',')

            # type of load [F, D, M]
            ty = app[0]
            start = float(app[1])
            if ty == 'F':
                if start <= x:
                    # apply load
                    eff = x - start
                    d += (1/6) * v * eff**3
            elif ty == 'D':
                end = float(app[2])
                if start <= x and x < end:
                    # apply load
                    eff = x - start
                    d += (1/24) * v * eff**4
            elif ty == 'M':
                if start <= x:
                    # apply load
                    eff = x - start
                    d += (1/6) * v * eff**2
            else:
                raise Exception(f"{ERROR_PREFIX} invalid force/moment key: '{k}'")
        return (1/(self.E * self.I)) * d
    
    def showForcesAndMoments(self):
        for k, v in self.ForcesAndMoments.items():
            print(f"{k}: {v}")

    def showParams(self):
        print(f"E = {self.E:.4f}Pa")
        print(f"I = {self.I:.4f}m^4")
        print(f"L = {self.L:.4f}m")
        
    def evaluate(self, n=1000):
        """Plots deflections and reports max deflection"""       
        x = np.linspace(0, self.L, num=n)

        # Data arrays
        beam = np.zeros(n)
        shear = np.zeros(n)
        moment = np.zeros(n)
        angle = np.zeros(n)
        deflection = np.zeros(n)
        
        # [loc, mag]
        max_shear = [0, 0]
        max_moment = [0, 0]
        max_angle = [0, 0]
        max_deflection = [0, 0]

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
