
from beam_analysis.AppliedLoad import DistributedLoad
from beam_analysis.Enums import AppliedLoadTypes, BeamAnalysisTypes, BoundaryConditionTypes


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

        if len(appliedLoads) > 0:
            self.AppliedLoads = appliedLoads
        else:
            self.AppliedLoads = []

        if len(boundaryConditions) > 0:
            self.BoundaryConditions = boundaryConditions
        else:
            self.BoundaryConditions = []

        self.C1 = 0
        self.C2 = 0
    

    def addAppliedLoad(self, appliedLoad):
        """
        `appliedLoad` - distributed load, point load, moment
        """
        # add counteracting distributed load to offset beyond a point of interest
        if type(appliedLoad) is AppliedLoadTypes.DISTRIBUTED_LOAD:
            counterLoad = DistributedLoad(appliedLoad.Stop, self.L, -appliedLoad.Magnitude)
            self.AppliedLoads.append(counterLoad)
        
        self.AppliedLoads.append(appliedLoad)


    def addBoundaryCondition(self, boundaryCondition):
        """
        `boundaryCondition` - BoundaryCondition to add
        """
        self.BoundaryConditions.append(boundaryCondition)


    def solve(self):
        """
        Requires a minimum of 2 boundary conditions to solve:

        - `ANGLE, DEFLECTION, ...`

        - `DEFLECTION, DEFLECTION, ...`
        """
        angleBcs = []
        deflectionBcs = []
        for bc in self.BoundaryConditions:
            if bc.Type == BoundaryConditionTypes.ANGLE:
                angleBcs.append(bc)
            elif bc.Type == BoundaryConditionTypes.DEFLECTION:
                deflectionBcs.append(bc)
        
        if 0 < len(angleBcs) and 0 < len(deflectionBcs):
            # use one angleBc and the first deflectionBc
            angleBc = angleBcs[0]
            deflectionBc = deflectionBcs[0]

            c1 = (angleBc.Value - self.evaluateAt(angleBc.Location, BeamAnalysisTypes.ANGLE, False)) * (self.E * self.I)
            self.C1 = c1
            self.C2 = (deflectionBc.Value - self.evaluateAt(deflectionBc.Location, BeamAnalysisTypes.DEFLECTION, False)) * (self.E * self.I) - c1*deflectionBc.Location

        elif 1 < len(deflectionBcs):
            # use first two deflection bcs
            deflectionBc1 = deflectionBcs[0]
            deflectionBc2 = deflectionBcs[1]

            defBc1K = (deflectionBc1.Value - self.evaluateAt(deflectionBc1.Location, BeamAnalysisTypes.DEFLECTION, includeConstants=False)) * (self.E * self.I)
            defBc2K = (deflectionBc2.Value - self.evaluateAt(deflectionBc2.Location, BeamAnalysisTypes.DEFLECTION, includeConstants=False)) * (self.E * self.I)
            
            c1 = (defBc1K - defBc2K) / (deflectionBc1.Location - deflectionBc2.Location)
            self.C1 = c1
            self.C2 = defBc1K - c1 * deflectionBc1.Location

        else:
            raise Exception(f"Invalid boundary conditions.\nEither one angle and one deflection condition, or two deflection conditions are required.\n{self.BoundaryConditions}")


    def evaluateAt(self, x, beamAnalysisType, includeConstants=True):
        """
        `x` - distance along the beam to evaluate the singularity function at

        `beamAnalysisType` - shear, moment, angle, deflection

        `includeConstants` - optionally exclude constants from calculations

        `NOTE` - to properly perform analysis, must call solve() before evaluating
        """
        val = 0
        if len(self.AppliedLoads) == 0:
            return val
        
        for load in self.AppliedLoads:
            val += load.evaluateAt(x, beamAnalysisType)
        
        if beamAnalysisType == BeamAnalysisTypes.ANGLE or beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
            if includeConstants:
                try:
                    if beamAnalysisType == BeamAnalysisTypes.ANGLE:
                        val += self.C1
                    else:
                        val += self.C1*x + self.C2
                except Exception as e:
                    raise Exception(f"unable to solve for singularity value when constants are not set.\n{e}")
            
            val /= (self.E * self.I)
        
        return val
    

    def getString(self, beamAnalysisType, includeConstants=True):
        """
        `beamAnalysisType` - shear, moment, angle, deflection

        `includeConstants` - optionally show only the loads

        returns a string representation of the singularity function
        """
        
        s = ""
        if len(self.AppliedLoads) == 0:
            return s
        
        for i in range(len(self.AppliedLoads)):
            load = self.AppliedLoads[i]
            if (load.Magnitude == 0):
                continue
            if (0 < i and 0 <= load.Magnitude):
                s += " + "
            elif (load.Magnitude < 0):
                s += " - "
            s += load.getString(beamAnalysisType)
        
        if includeConstants:
            if beamAnalysisType == BeamAnalysisTypes.ANGLE or beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
                if 0 <= self.C1:
                    s += f" + {self.C1}"
                else:
                    s += f" - {abs(self.C1)}"
            
            if beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
                if 0 <= self.C2:
                    s += f" + {self.C2}"
                else:
                    s += f" - {abs(self.C2)}"
        
        return s            
