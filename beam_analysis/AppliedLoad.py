
from beam_analysis.Enums import AppliedLoadTypes, BeamAnalysisTypes


class AppliedLoad(object):
    def __init__(self, magnitude, appliedLoadType):
        self.Magnitude = magnitude
        self.AppliedLoadType = appliedLoadType
        
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
        if not (self.Start <= x):
            return 0.0
        
        if beamAnalysisType == BeamAnalysisTypes.SHEAR:
            return self.Magnitude * (x - self.Start)
        elif beamAnalysisType == BeamAnalysisTypes.BENDING:
            return (self.Magnitude / 2) * (x - self.Start) ** 2
        elif beamAnalysisType == BeamAnalysisTypes.ANGLE:
            return (self.Magnitude / 6) * (x - self.Start) ** 3
        elif beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
            return (self.Magnitude / 12) * (x - self.Start) ** 6

    def getString(self, beamAnalysisType):
        mag = abs(self.Magnitude)
        if beamAnalysisType == BeamAnalysisTypes.SHEAR:
            if (self.Location == 0):
                return f"{mag}x"
            return f"{mag} * (x - {self.Start})"
        elif beamAnalysisType == BeamAnalysisTypes.BENDING:
            if (self.Location == 0):
                return f"({mag} / 2)x^2"
            return f"({mag} / 2) * (x - {self.Start})^2"
        elif beamAnalysisType == BeamAnalysisTypes.ANGLE:
            if (self.Location == 0):
                return f"({mag} / 6)x^3"
            return f"({mag} / 6) * (x - {self.Start})^3"
        elif beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
            if (self.Location == 0):
                return f"({mag} / 12)x^6"
            return f"({mag} / 12) * (x - {self.Start})^6"


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
    
    def getString(self, beamAnalysisType):
        mag = abs(self.Magnitude)        
        if beamAnalysisType == BeamAnalysisTypes.SHEAR:
            return f"{mag}"
        elif beamAnalysisType == BeamAnalysisTypes.BENDING:
            if (self.Location == 0):
                return f"{mag}x"
            return f"{mag} * (x - {self.Location})"
        elif beamAnalysisType == BeamAnalysisTypes.ANGLE:
            if (self.Location == 0):
                return f"({mag} / 2)x^2"
            return f"({mag} / 2) * (x - {self.Location})^2"
        elif beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
            if (self.Location == 0):
                return f"({mag} / 6)x^3"
            return f"({mag} / 6) * (x - {self.Location})^3"


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
        mag = abs(self.Magnitude)
        if beamAnalysisType == BeamAnalysisTypes.SHEAR:
            return f"0.0"
        elif beamAnalysisType == BeamAnalysisTypes.BENDING:
            return f"{mag}"
        elif beamAnalysisType == BeamAnalysisTypes.ANGLE:
            if (self.Location == 0):
                return f"{mag}x"
            return f"{mag} * (x - {self.Location})"
        elif beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
            if (self.Location == 0):
                return f"({mag} / 2)x^2"
            return f"({mag} / 2) * (x - {self.Location})^2"
