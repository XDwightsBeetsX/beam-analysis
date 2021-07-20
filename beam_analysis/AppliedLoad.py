

from enum import Enum


class AppliedLoad(object):
    def __init__(self, magnitude, appliedLoadType):
        def getPowerModifier(appliedLoadType):
            if appliedLoadType == AppliedLoadType.DISTRIBUTED_LOAD:
                return -1
            elif appliedLoadType == AppliedLoadType.POINT_LOAD:
                return 0
            elif appliedLoadType == AppliedLoadType.MOMENT:
                return 1
            else:
                raise Exception(f"Cannot create AppliedLoad without AppliedLoadType. provided {appliedLoadType}")
        
        self.Magnitude = magnitude
        self.AppliedLoadType = appliedLoadType
        self.PowerModifier = getPowerModifier(appliedLoadType)


class DistributedLoad(AppliedLoad):
    def __init__(self, start, stop, magnitude):
        super().__init__(self, magnitude, AppliedLoadType.DISTRIBUTED_LOAD)
        self.Start = start
        self.Stop = stop


class PointLoad(AppliedLoad):
    def __init__(self, location, magnitude):
        super().__init__(self, magnitude, AppliedLoadType.POINT_LOAD)
        self.Location = location


class Moment(AppliedLoad):
    def __init__(self, location, magnitude):
        super().__init__(self, magnitude, AppliedLoadType.MOMENT)
        self.Location = location


class AppliedLoadType(Enum):
    """
    The assigned values here matter and are used in Singularity analysis
    """
    DISTRIBUTED_LOAD = 1
    POINT_LOAD = 2
    MOMENT = 3
