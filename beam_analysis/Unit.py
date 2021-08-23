from enum import Enum


class UnitTypes(Enum):
    Shear = 1
    Bending = 2
    Angle = 3
    Deflection = 4


class Unit(object):
    def __init__(self, unitType, label):
        self.UnitType = unitType
        self.Label = label
    