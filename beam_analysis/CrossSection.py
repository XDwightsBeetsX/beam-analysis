import numpy as np
from enum import Enum


class CrossSectionTypes(Enum):
    RECT = 1
    CIRC = 2
    I = 3


class CrossSection(object):
    def __init__(self, crossSectionType, dims=None):
        """
        `crossSectionType` - a CrossSectionType object (CIRC, RECT, I, ...)

        `dims`  - CrossSection dimensions in form of an array/tuple:
            RECT    -   dims (width, height)
            
            CIRC    -   dims (radius)
        
            I       -   dims (beamWidth, beamHeight, flangeThickness, webThickness)
        """
        if not crossSectionType in set(cst for cst in CrossSectionTypes):
            raise Exception(f"Invalid crossSectionType: {crossSectionType}")
        
        self.CrossSectionType = crossSectionType
        
        if not dims or len(dims) == 0:
            raise Exception(f"Cannot create CrossSection {crossSectionType} without any dimensions")
        
        self.Dims = dims
    

    def getArea(self):
        if self.CrossSectionType == CrossSectionTypes.RECT:
            return self.Dims[0] * self.Dims[1]
        if self.CrossSectionType == CrossSectionTypes.CIRC:
            return np.pi * self.Dims[0]**2
        if self.CrossSectionType == CrossSectionTypes.I:
            # 2 x Flanges + Web
            return 2 * self.Dims[0] * self.Dims[2] + (self.Dims[1] - 2 * self.Dims[2]) * self.Dims[3]
    

    def getI(self):
        if self.CrossSectionType == CrossSectionTypes.RECT:
            return (1 / 12) * self.Dims[0] * self.Dims[1] **3
        if self.CrossSectionType == CrossSectionTypes.CIRC:
            return (np.pi / 4) * self.Dims[0] ** 4
        if self.CrossSectionType == CrossSectionTypes.I:
            wH = self.Dims[1] - 2 * self.Dims[2]  # inner web height
            iW = (1 / 12) * wH  # web inertia
            iF = (1 / 12) * (wH * self.Dims[2]**3) / 12 + (1 / 4) * self.Dims[2] * self.Dims[0] * self.Dims[3]**2  # flange inertia
            return iW + 2 * iF
    

    def getPlotPoints(self, xOffset, yOffset, zOffset, n=20):
        """
        returns n x,y,z points about the perimeter of the CrossSection
        """
        x, y, z = [], [], []
        if self.CrossSectionType == CrossSectionTypes.RECT:
            # TODO
            pass
        if self.CrossSectionType == CrossSectionTypes.CIRC:
            r = self.Dims[0]
            ith = 2 * np.pi / n  # radian fraction
            for i in range(0, n):
                x.append(xOffset)
                y.append(zOffset + np.cos(ith * i) * r)
                z.append(yOffset + np.sin(ith * i) * r)
            return x, y, z
        if self.CrossSectionType == CrossSectionTypes.I:
            # TODO
            pass
