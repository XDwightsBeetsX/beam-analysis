import numpy as np
from matplotlib import pyplot as plt
from numpy.core.fromnumeric import mean
from numpy.core.numeric import cross

from beam_analysis.Enums import BeamAnalysisTypes, Units
from beam_analysis.Singularity import Singularity
from beam_analysis.AppliedLoad import DistributedLoad, PointLoad, Moment
from beam_analysis.BoundaryCondition import BoundaryCondition
from beam_analysis.Unit import Unit
from beam_analysis.CrossSection import CrossSection, CrossSectionTypes
import beam_analysis.utils as utils


class Beam(object):
    """
    Primary class for the beam_analysis package.
    
    Add loads and perform analysis on this instance.
    """
    def __init__(self, l, e, i=None, crossSection=None):
        """
        `l` - Beam length

        `e` - Young's Modulus

        `i` - Moment of Intertia. Enter either this or give a crossSection.

        `crossSection` - a CrossSectionObject. This is preferred over a Moment of Inertia value (gives plot).
        """
        self.Tol = 1E-6
        self.L = l
        self.E = e

        if crossSection is not None:
            self.CrossSection = crossSection
            self.I = crossSection.getI()
        elif i is not None:
            self.CrossSection = CrossSection(CrossSectionTypes.CIRC, radius=1)
            self.I = i
        else:
            raise Exception("Unable to determine Moment of Intertia. Either I or a CrossSection is required.")
        

        self.SingularityXY = Singularity(l, e, self.I)
        self.SingularityXZ = Singularity(l, e, self.I)
        
        self.ShearUnits = Unit(Units.Shear, "[N]")
        self.MomentUnits = Unit(Units.Bending, "[N-m]")
        self.AngleUnits = Unit(Units.Angle, "[rad]")
        self.DeflectionUnits = Unit(Units.Deflection, "[m]")


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
        # =================================== #
        # = Solve for Singularity Constants = *
        # =================================== #
        pre = "[BEAM ANALYSIS] - "
        self.SingularityXY.solve()
        xySingularities = [
            self.SingularityXY.getString(BeamAnalysisTypes.SHEAR),
            self.SingularityXY.getString(BeamAnalysisTypes.BENDING),
            self.SingularityXY.getString(BeamAnalysisTypes.ANGLE),
            self.SingularityXY.getString(BeamAnalysisTypes.DEFLECTION)
        ]

        self.SingularityXZ.solve()
        xzSingularities = [
            self.SingularityXZ.getString(BeamAnalysisTypes.SHEAR),
            self.SingularityXZ.getString(BeamAnalysisTypes.BENDING),
            self.SingularityXZ.getString(BeamAnalysisTypes.ANGLE),
            self.SingularityXZ.getString(BeamAnalysisTypes.DEFLECTION)
        ]

        hasXY = not all(s == "" for s in xySingularities)
        hasXZ = not all(s == "" for s in xzSingularities)

        if not (hasXY or hasXZ):
            print("No analysis available in XY or XZ.")
            print("Quitting...")
            quit()
        

        # =================================== #
        # ========== Beam Results =========== #
        # =================================== #
        xVals = np.linspace(0, self.L, n)
        if hasXY:
            xyShear, xyBending, xyAngle, xyDeflection = [], [], [], []
            for x in xVals:
                xyShear.append(self.SingularityXY.evaluateAt(x, BeamAnalysisTypes.SHEAR))
                xyBending.append(self.SingularityXY.evaluateAt(x, BeamAnalysisTypes.BENDING))
                xyAngle.append(self.SingularityXY.evaluateAt(x, BeamAnalysisTypes.ANGLE))
                xyDeflection.append(self.SingularityXY.evaluateAt(x, BeamAnalysisTypes.DEFLECTION))
        
        if hasXZ:
            xzShear, xzBending, xzAngle, xzDeflection = [], [], [], []
            for x in xVals:
                xzShear.append(self.SingularityXZ.evaluateAt(x, BeamAnalysisTypes.SHEAR))
                xzBending.append(self.SingularityXZ.evaluateAt(x, BeamAnalysisTypes.BENDING))
                xzAngle.append(self.SingularityXZ.evaluateAt(x, BeamAnalysisTypes.ANGLE))
                xzDeflection.append(self.SingularityXZ.evaluateAt(x, BeamAnalysisTypes.DEFLECTION))
        

        # =================================== #
        # ========= Analysis Prompt ========= #
        # =================================== #
        sep = f"# {'='*len(xySingularities[3])} #"
        solving = "[SOLVING] - "
        if hasXY:
            print(sep)
            print(f"{pre}{solving}Solved for xy angle constant C1 = {self.SingularityXY.C1}")
            print(f"{pre}{solving}Solved for xy deflection constant C2 = {self.SingularityXY.C2}")
        
        if hasXZ:
            print(sep)
            print(f"{pre}{solving}Solved for xz angle constant C1 = {self.SingularityXZ.C1}")
            print(f"{pre}{solving}Solved for xz deflection constant C2 = {self.SingularityXZ.C2}")
        

        # =================================== #
        # ====== Singularity Functions ====== #
        # =================================== #
        if hasXY:
            print(sep)
            print(f"{pre}Singularity functions in XY plane:")
            for s in xySingularities:
                print(s)
        
        if hasXZ:
            print(sep)
            print(f"{pre}Singularity functions in XZ plane:")
            for s in xzSingularities:
                print(s)


        # =================================== #
        # ========= Analysis Report ========= #
        # =================================== #
        if hasXY:
            print(sep)
            print("Report in XY:")
            print(f"Maximum Shear in XY plane: {utils.getAbsMax(xyShear)} {self.ShearUnits.Label}")
            print(f"Maximum Moment in XY plane: {utils.getAbsMax(xyBending)} {self.MomentUnits.Label}")
            print(f"Maximum Angle in XY plane: {utils.getAbsMax(xyAngle)} {self.AngleUnits.Label}")
            print(f"Maximum Deflection in XY plane: {utils.getAbsMax(xyDeflection)} {self.DeflectionUnits.Label}")
        
        if hasXZ:
            print(sep)
            print("Report in XZ:")
            print(f"Maximum Shear in XZ plane: {utils.getAbsMax(xzShear)} {self.ShearUnits.Label}")
            print(f"Maximum Moment in XZ plane: {utils.getAbsMax(xzBending)} {self.MomentUnits.Label}")
            print(f"Maximum Angle in XZ plane: {utils.getAbsMax(xzAngle)} {self.AngleUnits.Label}")
            print(f"Maximum Deflection in XZ plane: {utils.getAbsMax(xzDeflection)} {self.DeflectionUnits.Label}")
        
        # done w console ouput
        print(sep)


        # =================================== #
        # ============ 2D Plots ============= #
        # =================================== #
        fig, axs = plt.subplots(4, 2, sharex='col', sharey='row')
        horizontal = [0] * n

        # plot styles
        beamStyle = 'k--'
        shearStyle = 'b-'
        bendingStyle = 'r-'
        angleStyle = 'y-'
        deflectionStyle = 'g-'

        if hasXY:
            axs[0, 0].set_title("XY Plane")
            axs[0, 0].plot(xVals, horizontal, beamStyle)
            axs[0, 0].plot(xVals, xyShear, shearStyle)
            axs[0, 0].set_ylabel(f"Shear {self.ShearUnits.Label}")

            axs[1, 0].plot(xVals, horizontal, beamStyle)
            axs[1, 0].plot(xVals, xyBending, bendingStyle)
            axs[1, 0].set_ylabel(f"Bending {self.MomentUnits.Label}")

            axs[2, 0].plot(xVals, horizontal, beamStyle)
            axs[2, 0].plot(xVals, xyAngle, angleStyle)
            axs[2, 0].set_ylabel(f"Angle {self.AngleUnits.Label}")

            axs[3, 0].plot(xVals, horizontal, beamStyle)
            axs[3, 0].plot(xVals, xyDeflection, deflectionStyle)
            axs[3, 0].set_ylabel(f"Deflection {self.DeflectionUnits.Label}")
        
        if hasXZ:
            axs[0, 1].set_title("XZ Plane")
            axs[0, 1].plot(xVals, horizontal, beamStyle)
            axs[0, 1].plot(xVals, xzShear, shearStyle)

            axs[1, 1].plot(xVals, horizontal, beamStyle)
            axs[1, 1].plot(xVals, xzBending, bendingStyle)

            axs[2, 1].plot(xVals, horizontal, beamStyle)
            axs[2, 1].plot(xVals, xzAngle, angleStyle)

            axs[3, 1].plot(xVals, horizontal, beamStyle)
            axs[3, 1].plot(xVals, xzDeflection, deflectionStyle)

        fig.tight_layout()
        plt.show()


        # =================================== #
        # ============ 3D Plot ============== #
        # =================================== #
        # calculate beam center coordinates
        # dict format { x = [y, z] }
        yzDeflectionByX = {}
        yDeflection = []
        zDeflection = []
        for i in range(n):
            yDef = 0
            zDef = 0
            if hasXY and hasXZ:
                yDef = xyDeflection[i]
                zDef = xzDeflection[i]
            elif hasXY:
                yDef = xyDeflection[i]
            elif hasXZ:
                zDef = xzDeflection[i]
            yDeflection.append(yDef)
            zDeflection.append(zDef)
            yzDeflectionByX[xVals[i]] = [yDef, zDef]
        
        # add beam mesh coordinates
        beam3d = [[], [], []]
        for ix in range(n):
            if ix % 5 == 0:
                xVal = xVals[ix]
                yzOffset = yzDeflectionByX[xVal]
                x, y, z = self.CrossSection.getPlotPoints(xVal, yzOffset[0], yzOffset[1])
                beam3d[0].extend(x)
                beam3d[1].extend(y)
                beam3d[2].extend(z)
                
        # PLOTTING
        # convention is that y is vertical in 2d and z is vertical in 3d, 
        # so swap to keep consistent feel across both
        fig3d = plt.figure()
        axs3d = fig3d.gca(projection='3d', box_aspect=(1, 1, 1))
        fig3d.suptitle("Beam Results", fontsize=16)
        # axs3d.set_aspect('equal')  # not yet implemented by matplotlib

        # centerlines
        axs3d.plot(xVals, [0]*n, [0]*n, 'k-')
        axs3d.plot(xVals, zDeflection, yDeflection, 'k--')

        # beam cross-sections
        axs3d.plot(beam3d[0], beam3d[1], beam3d[2], alpha=0.7)
        
        # use hack to make axes the same so that scale is right
        axs3d.plot(0, -self.L/2, -self.L/2)
        axs3d.plot(self.L, self.L/2, self.L/2)
        fig3d.tight_layout()

        plt.show()
