
import numpy as np
from matplotlib import pyplot as plt

from beam_analysis.Enums import BeamAnalysisTypes
from beam_analysis.Singularity import Singularity
from beam_analysis.AppliedLoad import DistributedLoad, PointLoad, Moment
from beam_analysis.BoundaryCondition import BoundaryCondition


class Beam(object):
    """
    Primary class for the beam_analysis package.
    
    Add loads and perform analysis on this instance.
    """
    def __init__(self, length, e, i):
        """
        `length` - Beam length

        `e` - Young's Modulus

        `i` - Moment of Intertia
        """
        self.L = length
        self.E = e
        self.I = i
        self.SingularityXY = Singularity(length, e, i)
        self.SingularityXZ = Singularity(length, e, i)
        self.Tol = 1E-6
    

    def addDistributedLoad(self, start, stop, magnitude, angle):
        """
        `start` - start distance of the distributed load
        
        `stop` - end distance of the distributed load
        
        `magnitude` - force of the distributed load

        `angle` - degrees in radians from the XY axis towards the XZ axis
        """
        if (start < 0 or self.L < stop or stop <= start):
            raise Exception(f"invalid start / stop for Distributed Load: {start} / {stop}")
        
        rads = angle * (np.pi / 180)
        xyComp = np.cos(rads)
        if (xyComp != 0):
            self.SingularityXY.addAppliedLoad(DistributedLoad(start, stop, xyComp * magnitude))
        
        xzComp = np.sin(rads)
        if (xzComp != 0):
            self.SingularityXZ.addAppliedLoad(DistributedLoad(start, stop, xzComp * magnitude))


    def addPointLoad(self, location, magnitude, angle):
        """
        `location` - the distance along the beam to the boundary condition

        `magnitude` - force of the applied load

        `angle` - degrees in radians from the XY axis towards the XZ axis
        """
        if (location < 0 or self.L < location):
            raise Exception(f"invalid location for Point Load: {location}")
        
        rads = angle * (np.pi / 180)
        xyComp = np.cos(rads)
        if (xyComp != 0):
            self.SingularityXY.addAppliedLoad(PointLoad(location, xyComp * magnitude))
        
        xzComp = np.sin(rads)
        if (xzComp != 0):
            self.SingularityXZ.addAppliedLoad(PointLoad(location, xzComp * magnitude))

    
    def addAppliedMoment(self, location, magnitude, angle):
        """
        `location` - the distance along the beam to the boundary condition
                
        `magnitude` - moment

        `angle` - degrees in radians from the XY axis towards the XZ axis
        """
        if (location < 0 or self.L < location):
            raise Exception(f"invalid location for Applied Moment: {location}")
        
        rads = angle * (np.pi / 180)
        xyComp = np.cos(rads)
        if (xyComp != 0):
            self.SingularityXY.addAppliedLoad(Moment(location, xyComp * magnitude))
        
        xzComp = np.sin(rads)
        if (xzComp != 0):
            self.SingularityXZ.addAppliedLoad(Moment(location, xzComp * magnitude))


    def addBoundaryCondition(self, location, boundaryConditionType, boundaryConditionValue):
        """
        `location` - the distance along the beam to the boundary condition

        `boundaryConditionType` - the type of the boundary condition. e.g: ANGLE, DEFLECTION

        `boundaryConditionValue` - the value of the boundary condition, typically 0
        """
        if (location < 0 or self.L < location):
            raise Exception(f"invalid location for Boundary Condition: {location}")
        
        self.SingularityXY.addBoundaryCondition(BoundaryCondition(location, boundaryConditionType, boundaryConditionValue))
        self.SingularityXZ.addBoundaryCondition(BoundaryCondition(location, boundaryConditionType, boundaryConditionValue))
    

    def runAnalysis(self, n=10**3):
        """
        `n` - optional number of data points to run the analysis, default is 10^3
        """
        self.SingularityXY.solve()
        self.SingularityXZ.solve()
        
        print("Singularity functions in XY plane:")
        print(self.SingularityXY.getString(BeamAnalysisTypes.SHEAR))
        print(self.SingularityXY.getString(BeamAnalysisTypes.BENDING))
        print(self.SingularityXY.getString(BeamAnalysisTypes.ANGLE))
        print(self.SingularityXY.getString(BeamAnalysisTypes.DEFLECTION))

        print("\nSingularity functions in XZ plane:")
        print(self.SingularityXZ.getString(BeamAnalysisTypes.SHEAR))
        print(self.SingularityXZ.getString(BeamAnalysisTypes.BENDING))
        print(self.SingularityXZ.getString(BeamAnalysisTypes.ANGLE))
        print(self.SingularityXZ.getString(BeamAnalysisTypes.DEFLECTION))

        xVals = np.linspace(0, self.L, n)
        beam2d = [0] * n
        xyShear, xyBending, xyAngle, xyDeflection = [], [], [], []
        xzShear, xzBending, xzAngle, xzDeflection = [], [], [], []

        for x in xVals:
            xyShear.append(self.SingularityXY.evaluateAt(x, BeamAnalysisTypes.SHEAR))
            xyBending.append(self.SingularityXY.evaluateAt(x, BeamAnalysisTypes.BENDING))
            xyAngle.append(self.SingularityXY.evaluateAt(x, BeamAnalysisTypes.ANGLE))
            xyDeflection.append(self.SingularityXY.evaluateAt(x, BeamAnalysisTypes.DEFLECTION))

            xzShear.append(self.SingularityXZ.evaluateAt(x, BeamAnalysisTypes.SHEAR))
            xzBending.append(self.SingularityXZ.evaluateAt(x, BeamAnalysisTypes.BENDING))
            xzAngle.append(self.SingularityXZ.evaluateAt(x, BeamAnalysisTypes.ANGLE))
            xzDeflection.append(self.SingularityXZ.evaluateAt(x, BeamAnalysisTypes.DEFLECTION))
        
        _fig, axs = plt.subplots(4, 2, sharex='col', sharey='row')
        
        # XY Plane
        axs[0, 0].set_title("XY Plane")
        axs[0, 0].plot(xVals, beam2d, 'k-')
        axs[0, 0].plot(xVals, xyShear)
        axs[0, 0].set_ylabel("Shear")

        axs[1, 0].plot(xVals, beam2d, 'k-')
        axs[1, 0].plot(xVals, xyBending)
        axs[1, 0].set_ylabel("Bending")

        axs[2, 0].plot(xVals, beam2d, 'k-')
        axs[2, 0].plot(xVals, xyAngle)
        axs[2, 0].set_ylabel("Angle")

        axs[3, 0].plot(xVals, beam2d, 'k-')
        axs[3, 0].plot(xVals, xyDeflection)
        axs[3, 0].set_ylabel("Deflection")

        # XZ Plane
        axs[0, 1].set_title("XZ Plane")
        axs[0, 1].plot(xVals, beam2d, 'k-')
        axs[0, 1].plot(xVals, xzShear)

        axs[1, 1].plot(xVals, beam2d, 'k-')
        axs[1, 1].plot(xVals, xzBending)

        axs[2, 1].plot(xVals, beam2d, 'k-')
        axs[2, 1].plot(xVals, xzAngle)

        axs[3, 1].plot(xVals, beam2d, 'k-')
        axs[3, 1].plot(xVals, xzDeflection)

        plt.show()
