from beam_analysis.AppliedLoad import AppliedLoadTypes, DistributedLoad
from beam_analysis.BeamAnalysisTypes import BeamAnalysisTypes
from beam_analysis.BoundaryCondition import BoundaryConditionTypes


class Singularity(object):
    def __init__(self, length, e, i):
        """
        `length` - Beam length

        `e` - Young's Modulus

        `i` - Moment of Intertia
        """
        self.L = length
        self.E = e
        self.I = i

        # defaults
        self.AppliedLoads = []
        self.BoundaryConditions = []
        self.C1 = None
        self.C2 = None
    

    def addAppliedLoad(self, appliedLoad):
        """
        `appliedLoad` - distributed load, point load, moment
        """
        self.AppliedLoads.append(appliedLoad)

        # add counteracting distributed load to offset beyond a point of interest
        if type(appliedLoad) is AppliedLoadTypes.DISTRIBUTED_LOAD:
            counterLoad = DistributedLoad(appliedLoad.Stop, self.L, -appliedLoad.Magnitude)
            self.AppliedLoads.append(counterLoad)


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

            c1 = (self.E * self.I) * (angleBc.Value - self.evaluateAt(angleBc.Location, BeamAnalysisTypes.ANGLE, includeConstants=False))
            c2 = (self.E * self.I) * (deflectionBc.Value - self.evaluateAt(deflectionBc.Location, BeamAnalysisTypes.DEFLECTION, includeConstants=False)) - (c1*deflectionBc.Location)
            
            self.C1 = c1
            self.C2 = c2

        elif 1 < len(deflectionBcs):
            # use first two deflection bcs
            deflectionBc1 = deflectionBcs[0]
            deflectionBc2 = deflectionBcs[1]

            defBc1K = (self.E * self.I) * (deflectionBc1.Value - self.evaluateAt(deflectionBc1.Location, BeamAnalysisTypes.DEFLECTION, includeConstants=False))
            defBc2K = (self.E * self.I) * (deflectionBc2.Value - self.evaluateAt(deflectionBc2.Location, BeamAnalysisTypes.DEFLECTION, includeConstants=False))
            
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

        `NOTE` - to properly perform angle and deflection analysis, must call solve() before evaluating
        """
        if len(self.AppliedLoads) == 0:
            return 0.0
        
        val = 0.0
        for load in self.AppliedLoads:
            val += load.evaluateAt(x, beamAnalysisType)
        
        if beamAnalysisType == BeamAnalysisTypes.ANGLE or beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
            if includeConstants:
                if beamAnalysisType == BeamAnalysisTypes.ANGLE:
                    val += self.C1
                else:
                    val += self.C1*x + self.C2
            val /= (self.E * self.I)
        
        return val
    

    def getString(self, beamAnalysisType, includeConstants=True):
        """
        `beamAnalysisType` - shear, moment, angle, deflection

        `includeConstants` - optionally show only the loads

        returns a string representation of the singularity function
        """
        equiv0 = 1e-14
        s = ""
        if len(self.AppliedLoads) == 0:
            return s
        
        for i in range(len(self.AppliedLoads)):
            load = self.AppliedLoads[i]
            if (abs(load.Magnitude) < equiv0):
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
