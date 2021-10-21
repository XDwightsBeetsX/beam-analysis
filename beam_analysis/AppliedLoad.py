from enum import Enum

from beam_analysis.BeamAnalysisTypes import BeamAnalysisTypes


class AppliedLoadTypes(Enum):
    """
    The assigned values here matter and are used in Singularity analysis
    """
    DISTRIBUTED_LOAD = 1
    POINT_LOAD = 2
    MOMENT = 3


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
        if beamAnalysisType == BeamAnalysisTypes.BENDING:
            return (self.Magnitude / 2) * (x - self.Start) ** 2
        if beamAnalysisType == BeamAnalysisTypes.ANGLE:
            return -(self.Magnitude / 6) * (x - self.Start) ** 3
        if beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
            return -(self.Magnitude / 24) * (x - self.Start) ** 4
    

    def getString(self, beamAnalysisType):
        mag = abs(self.Magnitude)
        if beamAnalysisType == BeamAnalysisTypes.SHEAR:
            if (self.Start == 0):
                return f"{mag}x"
            return f"{mag}<x - {self.Start}>^1"
        if beamAnalysisType == BeamAnalysisTypes.BENDING:
            if (self.Start == 0):
                return f"({mag} / 2)x^2"
            return f"({mag} / 2)<x - {self.Start}>^2"
        if beamAnalysisType == BeamAnalysisTypes.ANGLE:
            if (self.Start == 0):
                return f"({mag} / 6)x^3"
            return f"({mag} / 6)<x - {self.Start}>^3"
        if beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
            if (self.Start == 0):
                return f"({mag} / 24)x^4"
            return f"({mag} / 24)<x - {self.Start}>^4"


class PointLoad(AppliedLoad):
    def __init__(self, location, magnitude):
        super().__init__(magnitude, AppliedLoadTypes.POINT_LOAD)
        self.Location = location
    

    def evaluateAt(self, x, beamAnalysisType):
        if not (self.Location <= x):
            return 0.0
        if beamAnalysisType == BeamAnalysisTypes.SHEAR:
            return self.Magnitude
        if beamAnalysisType == BeamAnalysisTypes.BENDING:
            return self.Magnitude * (x - self.Location)
        if beamAnalysisType == BeamAnalysisTypes.ANGLE:
            return -(self.Magnitude / 2) * (x - self.Location) ** 2
        if beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
            return -(self.Magnitude / 6) * (x - self.Location) ** 3
    

    def getString(self, beamAnalysisType):
        mag = abs(self.Magnitude)        
        if beamAnalysisType == BeamAnalysisTypes.SHEAR:
            if (self.Location == 0):
                return f"{mag}"
            return f"{mag}<x - {self.Location}>^0"
        if beamAnalysisType == BeamAnalysisTypes.BENDING:
            return f"{mag}<x - {self.Location}>^1"
        if beamAnalysisType == BeamAnalysisTypes.ANGLE:
            return f"({mag} / 2)<x - {self.Location}>^2"
        if beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
            return f"({mag} / 6)<x - {self.Location}>^3"


class Moment(AppliedLoad):
    def __init__(self, location, magnitude):
        super().__init__(magnitude, AppliedLoadTypes.MOMENT)
        self.Location = location
    

    def evaluateAt(self, x, beamAnalysisType):
        if not (x <= self.Location):
            return 0.0
        if beamAnalysisType == BeamAnalysisTypes.SHEAR:
            return 0.0
        if beamAnalysisType == BeamAnalysisTypes.BENDING:
            return self.Magnitude
        if beamAnalysisType == BeamAnalysisTypes.ANGLE:
            return -self.Magnitude * (x - self.Location)
        if beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
            return -(self.Magnitude / 2) * (x - self.Location) ** 2
    

    def getString(self, beamAnalysisType):
        mag = abs(self.Magnitude)
        if beamAnalysisType == BeamAnalysisTypes.SHEAR:
            return f"0.0"
        if beamAnalysisType == BeamAnalysisTypes.BENDING:
            if (self.Location == 0):
                return f"{mag}"
            return f"{mag}<x - {self.Location}>^0"
        if beamAnalysisType == BeamAnalysisTypes.ANGLE:
            return f"{mag}<x - {self.Location}>^1"
        if beamAnalysisType == BeamAnalysisTypes.DEFLECTION:
            return f"({mag} / 2)<x - {self.Location}>^2"
