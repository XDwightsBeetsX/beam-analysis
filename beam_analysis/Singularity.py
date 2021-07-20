
import numpy as np

from beam_analysis.AppliedLoad import AppliedLoadType, DistributedLoad, Moment
from beam_analysis.Beam import BeamAnalysisTypes


class Singularity(object):
    def __init__(self, length, e, i, appliedLoads=[], boundaryConditions=[]):
        """
        `length` - Beam length

        `e` - Young's Modulus

        `i` - Moment of Intertia

        `appliedLoads` - (optional) a list of AppliedLoads in this Singularity Eq'n

        `boundaryConditions` - (optional) a list of BoundaryConditions in this Singularity Eq'n
        """
        self.L = length
        self.E = e
        self.I = i
        self.AppliedLoads = appliedLoads
        self.BoundaryConditions = boundaryConditions
    

    def addAppliedLoad(self, appliedLoad):
        """
        `appliedLoad` - distributed load, point load, moment
        """
        if type(appliedLoad) is AppliedLoadType.DISTRIBUTED_LOAD:
            counterLoad = DistributedLoad(appliedLoad.stop, self.L, -appliedLoad.Magnitude)
            self.AppliedLoads.append(counterLoad)
        self.AppliedLoads.append(appliedLoad)


    def addBoundaryCondition(self, boundaryCondition):
        """
        `boundaryCondition` - BoundaryCondition to add
        """
        self.BoundaryConditions.append(boundaryCondition)


    def evaluateAt(self, x, beamAnalysisType):
        """
        `x` - distance along the beam to evaluate the singularity function at

        `beamAnalysisType` - shear, moment, angle, deflection
        """
        val = 0
        
        for load in self.AppliedLoads:
            t = type(load)
            # beamAnalysisType follows  0, 1, 2, 3
            # AppliedLoadType follows   1, 2, 3
            if t is AppliedLoadType.DISTRIBUTED_LOAD:
                if (load.Start <= x and x <= load.Stop):
                    val += (load.Magnitude / load.PowerModifier) * (x - load.Start) ** (beamAnalysisType.value + load.PowerModifier)
            
            elif t is AppliedLoadType.POINT_LOAD:
                if (x == load.location):
                    val += (load.Magnitude / load.PowerModifier) * (x) ** (beamAnalysisType.value + load.PowerModifier)

            elif t is AppliedLoadType.MOMENT:
                if (x == load.location):
                    val += (load.Magnitude / load.PowerModifier) * (x) ** (beamAnalysisType.value + load.PowerModifier)
            
        return val
    

    def getString(self, beamAnalysisType):
        """
        `beamAnalysisType` - shear, moment, angle, deflection

        returns a string representation of the singularity function
        """
        s = ""
        for i in range(len(self.AppliedLoads)):
            load = self.AppliedLoads[i]
            t = type(load)
            # beamAnalysisType follows  0, 1, 2, 3
            # AppliedLoadType follows   1, 2, 3
            if t is AppliedLoadType.DISTRIBUTED_LOAD:
                s += f"({load.Magnitude} / {load.PowerModifier}) * <x - {load.Start}>^{beamAnalysisType.value + load.PowerModifier}"
            
            elif t is AppliedLoadType.POINT_LOAD:
                s += f"({load.Magnitude} / {load.PowerModifier}) * x^{beamAnalysisType.value + load.PowerModifier}"

            elif t is AppliedLoadType.MOMENT:
                s += f"({load.Magnitude} / {load.PowerModifier}) * x^{beamAnalysisType.value + load.PowerModifier}"
            
            if i != len(self.AppliedLoads)-1:
                s += " + "
        
        return s            
