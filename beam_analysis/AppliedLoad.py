
from beam_analysis.Enums import AppliedLoadTypes, BeamAnalysisTypes


class AppliedLoad(object):
    def __init__(self, magnitude, appliedLoadType):
        def getPowerModifier(appliedLoadType):
            if appliedLoadType == AppliedLoadTypes.DISTRIBUTED_LOAD:
                return -1
            elif appliedLoadType == AppliedLoadTypes.POINT_LOAD:
                return 0
            elif appliedLoadType == AppliedLoadTypes.MOMENT:
                return 1
            else:
                raise Exception(f"Cannot create AppliedLoad without AppliedLoadType. provided {appliedLoadType}")
        
        self.Magnitude = magnitude
        self.AppliedLoadType = appliedLoadType
        self.PowerModifier = getPowerModifier(appliedLoadType)
    
    def evaluateAt(self, x, beamAnalysisType):
        pass
    def getString(self, beamAnalysisType):
        pass


class DistributedLoad(AppliedLoad):
    def __init__(self, start, stop, magnitude):
        super().__init__(magnitude, AppliedLoadTypes.DISTRIBUTED_LOAD)
        self.Start = start
        self.Stop = stop
    
    def evaluateAt(self, x, beamAnalysisType):
        if not (self.Start <= x and x <= self.Stop):
            return 0.0
        
        if beamAnalysisType == BeamAnalysisTypes.SHEAR:
            return self.Magnitude * (x - self.Start)
        elif beamAnalysisType == BeamAnalysisTypes.BENDING:
            return (self.Magnitude / 2) * (x - self.Start) ** 2
        elif beamAnalysisType == BeamAnalysisTypes.ANGLE:
            return (self.Magnitude / 6) * (x - self.Start) ** 3
        elif beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
            return (self.Magnitude / 12) * (x - self.Start) ** 6


class PointLoad(AppliedLoad):
    def __init__(self, location, magnitude):
        super().__init__(magnitude, AppliedLoadTypes.POINT_LOAD)
        self.Location = location
    
    def evaluateAt(self, x, beamAnalysisType):
        if not (x <= self.Location):
            return 0.0
        
        if beamAnalysisType == BeamAnalysisTypes.SHEAR:
            return self.Magnitude
        elif beamAnalysisType == BeamAnalysisTypes.BENDING:
            return self.Magnitude * (x - self.Location)
        elif beamAnalysisType == BeamAnalysisTypes.ANGLE:
            return (self.Magnitude / 2) * (x - self.Location) ** 2
        elif beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
            return (self.Magnitude / 6) * (x - self.Location) ** 3


class Moment(AppliedLoad):
    def __init__(self, location, magnitude):
        super().__init__(magnitude, AppliedLoadTypes.MOMENT)
        self.Location = location
    
    def evaluateAt(self, x, beamAnalysisType):
        if not (x <= self.Location):
            return 0.0
        
        if beamAnalysisType == BeamAnalysisTypes.SHEAR:
            return 0.0
        elif beamAnalysisType == BeamAnalysisTypes.BENDING:
            return self.Magnitude
        elif beamAnalysisType == BeamAnalysisTypes.ANGLE:
            return self.Magnitude * (x - self.Location)
        elif beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
            return (self.Magnitude / 2) * (x - self.Location) ** 2
    
    def getString(self, beamAnalysisType):
        pass
