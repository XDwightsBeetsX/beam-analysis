
import numpy as np
from matplotlib import pyplot as plt

from beam_analysis.Enums import Planes, BeamAnalysisTypes, BoundaryConditionTypes

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
    

    def addDistributedLoad(self, start, stop, magnitude, plane):
        """
        `start` - start distance of the distributed load
        
        `stop` - end distance of the distributed load
        
        `magnitude` - force of the distributed load

        `plane` - the area in which the laod acts. XY, XZ
        """
        if plane == Planes.XY:
            self.SingularityXY.addAppliedLoad(DistributedLoad(start, stop, magnitude))
        elif plane == Planes.XZ:
            self.SingularityXZ.addAppliedLoad(DistributedLoad(start, stop, magnitude))
        else:
            raise Exception(f"invalid parameters: {start}, {stop}, {magnitude}, {plane}")


    def addPointLoad(self, location, magnitude, plane):
        """
        `location` - the distance along the beam to the boundary condition

        `magnitude` - force of the applied load

        `plane` - the area in which the laod acts. XY, XZ
        """
        newPointLoad = PointLoad(location, magnitude)
        if plane == Planes.XY:
            self.SingularityXY.addAppliedLoad(newPointLoad)
        elif plane == Planes.XZ:
            self.SingularityXZ.addAppliedLoad(newPointLoad)
        else:
            raise Exception(f"invalid parameters: {location}, {magnitude}, {plane}")


    def addAppliedMoment(self, location, magnitude, plane):
        """
        `location` - the distance along the beam to the boundary condition
                
        `magnitude` - moment

        `plane` - the area in which the laod acts. XY, XZ
        """
        newMoment = Moment(location, magnitude)
        if plane == Planes.XY:
            self.SingularityXY.addAppliedLoad(newMoment)
        elif plane == Planes.XZ:
            self.SingularityXZ.addAppliedLoad(newMoment)
        else:
            raise Exception(f"invalid parameters: {location}, {magnitude}, {plane}")
    

    def addBoundaryCondition(self, location, boundaryConditionType, boundaryConditionValue, plane):
        """
        `location` - the distance along the beam to the boundary condition

        `boundaryConditionType` - the type of the boundary condition. e.g: ANGLE, DEFLECTION

        `boundaryConditionValue` - the value of the boundary condition, typically 0

        `plane` - the area in which the laod acts. XY, XZ
        """
        if plane == Planes.XY:
            self.SingularityXY.addBoundaryCondition(BoundaryCondition(location, boundaryConditionType, boundaryConditionValue))
        elif plane == Planes.XZ:
            self.SingularityXZ.addBoundaryCondition()(BoundaryCondition(location, boundaryConditionType, boundaryConditionValue))
        else:
            raise Exception(f"invalid parameters: {location}, {boundaryConditionType}, {boundaryConditionValue}, {plane}")
    

    def runAnalysis(self, n=10**3, showAnalysisLog=True):
        """
        `n` - optional number of data points to run the analysis, default is 10^3
        
        `showAnalysisLog` - toggle console output notifications, basically the Singularity functions. (report displays regardless)
        """
        xVals = np.linspace(0, self.L, n)

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
        
        plt.plot(xVals, xyShear, xVals, xyBending)
        plt.show()
