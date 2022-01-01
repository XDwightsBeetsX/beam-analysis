import os
import numpy as np
from matplotlib import pyplot as plt

from beam_analysis.BeamAnalysisTypes import BeamAnalysisTypes
from beam_analysis.Singularity import Singularity
from beam_analysis.AppliedLoad import DistributedLoad, PointLoad, Moment
from beam_analysis.BoundaryCondition import BoundaryCondition
from beam_analysis.Unit import Unit, UnitTypes
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
            self.CrossSection = CrossSection(CrossSectionTypes.CIRC, dims=[1])
            self.I = i
        else:
            raise Exception("Unable to determine Moment of Intertia. Either I or a CrossSection is required.")
        

        self.SingularityXY = Singularity(l, e, self.I)
        self.SingularityXZ = Singularity(l, e, self.I)
        
        self.ShearUnits = Unit(UnitTypes.Shear, "[N]")
        self.MomentUnits = Unit(UnitTypes.Bending, "[N-m]")
        self.AngleUnits = Unit(UnitTypes.Angle, "[rad]")
        self.DeflectionUnits = Unit(UnitTypes.Deflection, "[m]")


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
    

    def runAnalysis(self, n=10**3, showPlots=True, outputToFile=False):
        """
        `n` - optional number of data points to run the analysis, default is 10^3
        """
        pre = "[BEAM ANALYSIS] - "
        print(f"{pre}Running analysis with beam parameters:")
        
        bL = "length:"
        bE = "Young's modulus of material:"
        bI = "Moment of inertia:"
        print(f"{pre}{bL:30} {self.L}")
        print(f"{pre}{bE:30} {self.E}")
        print(f"{pre}{bI:30} {self.I}")

        # =================================== #
        # = Solve for Singularity Constants = *
        # =================================== #
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

        # determine if there is any anlaysis to run
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
        # ============= Report ============== #
        # =================================== #
        pre_solving = "[SOLVING] - "
        mS = "Max Shear:"
        mM = "Max Moment:"
        mA = "Max Angle:"
        mD = "Max Deflection:"
        sep = f"# {'='*max(len(xySingularities[3]), len(xzSingularities[3]))} #"
        
        # digits to round to
        rdSh = 3
        rdB = 3
        rdA = 5
        rdD = 5

        # write singularity constants in XY to console
        if hasXY:
            print(sep)
            print(f"{pre}{pre_solving}Solved for xy angle constant C1 = {self.SingularityXY.C1}")
            print(f"{pre}{pre_solving}Solved for xy deflection constant C2 = {self.SingularityXY.C2}")
        
        # write singularity constants in XZ to console
        if hasXZ:
            print(sep)
            print(f"{pre}{pre_solving}Solved for xz angle constant C1 = {self.SingularityXZ.C1}")
            print(f"{pre}{pre_solving}Solved for xz deflection constant C2 = {self.SingularityXZ.C2}")
        
        # write singularities in XY to console
        if hasXY:
            print(sep)
            print(f"{pre}Singularity functions in XY:")
            for s in xySingularities:
                print(s)
        
        # write singularities in XZ to console
        if hasXZ:
            print(sep)
            print(f"{pre}Singularity functions in XZ:")
            for s in xzSingularities:
                print(s)
        
        # write max vals in XY to console
        if hasXY:
            mSxy = utils.getAbsMax(xyShear, rdSh)
            mBxy = utils.getAbsMax(xyBending, rdB)
            mAxy = utils.getAbsMax(xyAngle, rdA)
            mDxy = utils.getAbsMax(xyDeflection, rdD)

            print(sep)
            print(f"{pre}Report in XY:")
            print(f"{mS:20} {mSxy:10} {self.ShearUnits.Label}")
            print(f"{mM:20} {mBxy:10} {self.MomentUnits.Label}")
            print(f"{mA:20} {mAxy:10} {self.AngleUnits.Label}")
            print(f"{mD:20} {mDxy:10} {self.DeflectionUnits.Label}")
        
        # write max vals in XZ to console
        if hasXZ:
            mSxz = utils.getAbsMax(xzShear, rdSh)
            mBxz = utils.getAbsMax(xzBending, rdB)
            mAxz = utils.getAbsMax(xzAngle, rdA)
            mDxz = utils.getAbsMax(xzDeflection, rdD)

            print(sep)
            print(f"{pre}Report in XZ:")
            print(f"{mS:20} {mSxz:10} {self.ShearUnits.Label}")
            print(f"{mM:20} {mBxz:10} {self.MomentUnits.Label}")
            print(f"{mA:20} {mAxz:10} {self.AngleUnits.Label}")
            print(f"{mD:20} {mDxz:10} {self.DeflectionUnits.Label}")
        
        # done w console ouput
        print(sep)

        # Show plots of XY/XZ params & final beam deflection
        if showPlots:
            print(f"{pre}generating beam plots...")
            xyParams = (xyShear, xyBending, xyAngle, xyDeflection)
            xzParams = (xzShear, xzBending, xzAngle, xzDeflection)
            self.showPlots(xVals, xyParams, xzParams)
            print(f"done.")
        
        # if desired, output results to .csv file
        if outputToFile:
            # if the output folder doesnt exist, create it
            outputFolderName = "beam-analysis-results"
            if not os.path.exists(outputFolderName):
                os.makedirs(outputFolderName)
            
            # generate filename from beam params
            print(f"{pre}outputting to file in {outputFolderName}/...")
            filename = outputFolderName + "/" + f"beam-analysis-results-l{self.L}-cs{self.CrossSection.CrossSectionType.name}".replace('.', '_') + ".csv"
            
            # write the mS, mB, mA, MD vals for XY and XZ as well as some beam params
            with open(filename, 'w') as resultsFile:
                resultsFile.write("Beam Analysis Results\n")
                
                resultsFile.write("\n")
                
                resultsFile.write("Beam\n")
                resultsFile.write(f"length:, {self.L}\n")
                resultsFile.write(f"cross-section:, {self.CrossSection.CrossSectionType.name}\n")
                resultsFile.write(f"E:, {self.E}\n")
                resultsFile.write(f"I:, {self.I}\n") 
                
                resultsFile.write("\n")

                # loads in XY
                if hasXY:
                    resultsFile.write("Applied Loads in XY\n")
                    resultsFile.write("Load Type, Start, Stop, Magnitude\n")
                    for load in self.SingularityXY.AppliedLoads:
                        if isinstance(load, DistributedLoad):
                            resultsFile.write(f"{load.AppliedLoadType.name}, {load.Start}, {load.Stop}, {load.Magnitude}\n")
                        else:
                            resultsFile.write(f"{load.AppliedLoadType.name}, {load.Location}, N/A, {load.Magnitude}\n")
                    resultsFile.write("\n")
                
                # loads in XZ
                if hasXZ:
                    resultsFile.write("Applied Loads in XZ\n")
                    resultsFile.write("Load Type, Start, Stop, Magnitude\n")
                    for load in self.SingularityXZ.AppliedLoads:
                        if isinstance(load, DistributedLoad):
                            resultsFile.write(f"{load.AppliedLoadType.name}, {load.Start}, {load.Stop}, {load.Magnitude}\n")
                        else:
                            resultsFile.write(f"{load.AppliedLoadType.name}, {load.Location}, N/A, {load.Magnitude}\n")
                    resultsFile.write("\n")
                
                # max vals in XY
                if hasXY:
                    resultsFile.write("XY Plane\n")
                    resultsFile.write(f"{mS} {self.ShearUnits}, {mSxy}\n")
                    resultsFile.write(f"{mM} {self.MomentUnits}, {mBxy}\n")
                    resultsFile.write(f"{mA} {self.AngleUnits}, {mAxy}\n")
                    resultsFile.write(f"{mD} {self.DeflectionUnits}, {mDxy}\n")
                    resultsFile.write("\n")
                
                # max vals in XZ
                if hasXZ:
                    resultsFile.write("XZ Plane\n")
                    resultsFile.write(f"{mS} {self.ShearUnits}, {mSxz}\n")
                    resultsFile.write(f"{mM} {self.MomentUnits}, {mBxz}\n")
                    resultsFile.write(f"{mA} {self.AngleUnits}, {mAxz}\n")
                    resultsFile.write(f"{mD} {self.DeflectionUnits}, {mDxz}\n")
                    resultsFile.write("\n")
            print(f"done.")  

    
    def showPlots(self, xVals, xyParams, xzParams, w=12, h=6):
        """
        Makes plots of beam params and a 3d plot of final beam deflection.

        `xVals` - a linspace of points along the beam (x-axis)

        `xyParams` - a tuple of singularity values in xy: (xyShear, xyBending, xyAngle, xyDeflection)

        `xzParams` - a tuple of singularity values in xz: (xzShear, xzBending, xzAngle, xzDeflection)
        """
        """
        PLOT LAYOUT
        |    XY      |     XZ     |     3D Plot       |
        |   Shear    |   Shear    |    |  /           |
        |  Bending   |  Bending   |    | /            |
        |   Angle    |   Angle    |    |/__________   |
        | Deflection | Deflection |   /|              |
        """
        # Main Fig -> 1x2 figs (2D/3D)
        # Left Fig -> 2x4 figs (XY/XZ plots)
        # Right Fig -> 1x1 fig (3D plot)
        fig_main = plt.figure(figsize=(w, h))
        fig_main.suptitle("Beam Analysis Results")
        
        fig_left, fig_right = fig_main.subfigures(nrows=1, ncols=2)
        fig_left.suptitle("2D")
        fig_right.suptitle("3D")

        # =================================== #
        # ============ 2D Plots ============= #
        # =================================== #
        ax2d = fig_left.subplots(4, 2, sharex='col', sharey='row')
        ax2d[0, 0].set_title("XY Plane")
        ax2d[0, 1].set_title("XZ Plane")

        # std plot params
        n = len(xVals)
        axis0 = [0]*n

        # plot styles
        beamStyle = 'k--'
        shearStyle = 'b-'
        bendingStyle = 'r-'
        angleStyle = 'y-'
        deflectionStyle = 'g-'
        
        # plot Shear, Bending, Angle, and Deflection in 2D
        # XY on left, XZ on right
        ax2d[0, 0].set_ylabel(f"Shear {self.ShearUnits.Label}")
        ax2d[0, 0].plot(xVals, axis0, beamStyle)
        ax2d[0, 0].plot(xVals, xyParams[0], shearStyle)
        
        ax2d[1, 0].set_ylabel(f"Bending {self.MomentUnits.Label}")
        ax2d[1, 0].plot(xVals, axis0, beamStyle)
        ax2d[1, 0].plot(xVals, xyParams[1], bendingStyle)
        
        ax2d[2, 0].set_ylabel(f"Angle {self.AngleUnits.Label}")
        ax2d[2, 0].plot(xVals, axis0, beamStyle)
        ax2d[2, 0].plot(xVals, xyParams[2], angleStyle)

        ax2d[3, 0].set_ylabel(f"Deflection {self.DeflectionUnits.Label}")
        ax2d[3, 0].plot(xVals, axis0, beamStyle)
        ax2d[3, 0].plot(xVals, xyParams[3], deflectionStyle)

        ax2d[0, 1].plot(xVals, axis0, beamStyle)
        ax2d[0, 1].plot(xVals, xzParams[0], shearStyle)

        ax2d[1, 1].plot(xVals, axis0, beamStyle)
        ax2d[1, 1].plot(xVals, xzParams[1], bendingStyle)

        ax2d[2, 1].plot(xVals, axis0, beamStyle)
        ax2d[2, 1].plot(xVals, xzParams[2], angleStyle)

        ax2d[3, 1].plot(xVals, axis0, beamStyle)
        ax2d[3, 1].plot(xVals, xzParams[3], deflectionStyle)

        fig_left.align_ylabels()

        
        # =================================== #
        # ============ 3D Plot ============== #
        # =================================== #
        ax3d = fig_right.add_subplot(111, projection='3d')

        # convention is that y is vertical in 2d and z is vertical in 3d, 
        # so swap to keep consistent feel across both
        ax3d.set_xlabel("X")
        ax3d.set_ylabel("Z")
        ax3d.set_zlabel("Y")
        
        # calculate beam center coordinates
        # dict format { x = [y, z] }
        yzDeflectionByX = {}
        for i in range(n):
            yzDeflectionByX[xVals[i]] = [xyParams[3][i], xzParams[3][i]]
        
        # add beam mesh coordinates
        beam3d = [[], [], []]
        for ix in range(n):
            if ix % 5 == 0:
                xVal = xVals[ix]
                yOffset, zOffset = yzDeflectionByX[xVal]
                x, y, z = self.CrossSection.getPlotPoints(xVal, yOffset, zOffset)
                beam3d[0].extend(x)
                beam3d[1].extend(y)
                beam3d[2].extend(z)
        
        # plot beam centerline and cross-sections
        ax3d.plot(xVals, xzParams[3], xyParams[3], 'k--')
        ax3d.plot(beam3d[0], beam3d[1], beam3d[2], 'b-', alpha=0.7)
        
        # axis lines
        axMax = self.L/2
        axPerp = np.linspace(-axMax, axMax, n)
        ax3d.plot(xVals, axis0, axis0, 'k-')
        ax3d.plot(axis0, axPerp, axis0, 'k-')
        ax3d.plot(axis0, axis0, axPerp, 'k-')

        # set axis scale
        ax3d.set_xlim(0, self.L)
        ax3d.set_ylim(-axMax, axMax)
        ax3d.set_zlim(-axMax, axMax)

        # size to fit ylabels on left
        plt.subplots_adjust(left=0.2, right=0.9)
        plt.show()
