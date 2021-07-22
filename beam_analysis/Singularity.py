
from beam_analysis.Enums import AppliedLoadTypes


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
        if type(appliedLoad) is AppliedLoadTypes.DISTRIBUTED_LOAD:
            counterLoad = AppliedLoadTypes(appliedLoad.stop, self.L, -appliedLoad.Magnitude)
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
            val += load.evaluateAt(x, beamAnalysisType)
        return val
    

    def getString(self, beamAnalysisType):
        """
        `beamAnalysisType` - shear, moment, angle, deflection

        returns a string representation of the singularity function
        """
        s = ""
        for i in range(len(self.AppliedLoads)):
            s += self.AppliedLoads[i].getString(beamAnalysisType)
            
            if i != len(self.AppliedLoads)-1:
                s += " + "
        return s            
