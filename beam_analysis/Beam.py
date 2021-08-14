
import numpy as np
from matplotlib import pyplot as plt

from beam_analysis.Enums import BeamAnalysisTypes, Units
from beam_analysis.Singularity import Singularity
from beam_analysis.AppliedLoad import DistributedLoad, PointLoad, Moment
from beam_analysis.BoundaryCondition import BoundaryCondition
from beam_analysis.Unit import Unit
from beam_analysis.utils import getAbsMax


class Beam(object):
    """
    Primary class for the beam_analysis package.
    
    Add loads and perform analysis on this instance.
    """
    def __init__(self, l, e, i, unitsFrom="m", unitsTo="c"):
        """
        `l` - Beam length

        `e` - Young's Modulus

        `i` - Moment of Intertia

        `unitsFrom / unitsTo` - "m(etric)" or "c(ustomary)" conversions available
        """
        self.Tol = 1E-6

        self.L = l
        self.E = e
        self.I = i
        
        self.SingularityXY = Singularity(l, e, i)
        self.SingularityXZ = Singularity(l, e, i)
        
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
            quit()
        

        # =================================== #
        # ========== Beam Results =========== #
        # =================================== #
        # independent vars
        xVals = np.linspace(0, self.L, n)
        # dependent decl
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
        

        # =================================== #
        # ========= Analysis Prompt ========= #
        # =================================== #
        sep = f"# {'='*len(xySingularities[3])} #"
        solving = "[SOLVING] - "
        print(sep)
        print(f"{pre}{solving}Solved for xy angle constant C1 = {self.SingularityXY.C1}")
        print(f"{pre}{solving}Solved for xy deflection constant C2 = {self.SingularityXY.C2}")

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
        print(sep)


        # =================================== #
        # ========= Analysis Report ========= #
        # =================================== #
        if hasXY:
            print("Report in XY:")
            print(f"Maximum Shear in XY plane: {getAbsMax(xyShear)} {self.ShearUnits}")
            print(f"Maximum Moment in XY plane: {getAbsMax(xyBending)} {self.MomentUnits}")
            print(f"Maximum Angle in XY plane: {getAbsMax(xyAngle)} {self.AngleUnits}")
            print(f"Maximum Deflection in XY plane: {getAbsMax(xyDeflection)} {self.DeflectionUnits}")
        if hasXZ:
            print("Report in XZ:")
            print(f"Maximum Shear in XZ plane: {getAbsMax(xzShear)} {self.ShearUnits}")
            print(f"Maximum Moment in XZ plane: {getAbsMax(xzBending)} {self.MomentUnits}")
            print(f"Maximum Angle in XZ plane: {getAbsMax(xzAngle)} {self.AngleUnits}")
            print(f"Maximum Deflection in XZ plane: {getAbsMax(xzDeflection)} {self.DeflectionUnits}")
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
        res = 8    # angles per beam cross-section "slice"
        angles = np.linspace(0, np.pi, res)
        beam3d = [xVals, xyDeflection, xzDeflection]
        shear3d, bending3d = [], []
        
        # for theta in angles:
            # for i_x in range(n):
                # shear3d.append([xVals[i], xyShear[i]*np.sin(t) + xzShear[i]*np.sin(t), xyShear[i]*np.cos(t) + xzShear[i]*np.cos(t)])
                # bending3d.append([xVals[i], xyBending[i]*np.sin(t) + xyBending[i]*np.sin(t), xyBending[i]*np.cos(t) + xyBending[i]*np.cos(t)])
           
                
        # Plot lines in 3d
        # convention is that y is vertical in 2d and z is vertical in 3d, so swap to keep consistent feel across both
        fig3d = plt.figure()
        axs3d = fig3d.gca(projection='3d', box_aspect=(1, 1, 1))
        
        axs3d.plot(xVals, horizontal, horizontal, 'k--')
        axs3d.plot(beam3d[0], beam3d[2], beam3d[1], 'k--', alpha=0.5)
        
        # for i_theta in range(res):  
            # axs3d.plot(shear3d[0], shear3d[1], shear3d[2], 'b-')
            # axs3d.plot(bending3d[0], bending3d[1], bending3d[2], 'r-')
        
        fig3d.tight_layout()
        plt.show()
