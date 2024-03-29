"""
TODO this is not in use by the package but may be incoorperated later...
"""


class StressElement(object):
    def __init__(self, sigmaX, sigmaY, sigmaZ, shearXY=0, shearYZ=0, shearZX=0):
        self.SigmaX = sigmaX
        self.SigmaY = sigmaY
        self.SigmaZ = sigmaZ
        self.ShearXY = shearXY
        self.ShearYZ = shearYZ
        self.ShearZX = shearZX
        # obtain principle stresses
        if shearXY == 0 and shearYZ == 0 and shearZX == 0:
            self.Sigma1 = sigmaX
            self.Sigma2 = sigmaY
            self.Sigma3 = sigmaZ
            self.R = 0
        else:
            avg = (sigmaX + sigmaY) / 2
            r = (((sigmaX - sigmaY) / 2)**2 + shearXY**2)**.5
            self.Sigma1 = avg + r
            self.Sigma2 = avg - r
            self.Sigma3 = 0
            self.R = r
        
        print(f"Sigma1:         {self.Sigma1}")
        print(f"Sigma2:         {self.Sigma2}")
        print(f"Sigma3:         {self.Sigma3}")
        print(f"R:              {self.R}")
    

    def setYieldStrength(self, yieldStrength):
        """
        !! Ensure consistend units with StressElement obj !!
        """
        self.YieldStrength = yieldStrength
    

    def getFos(self, appliedStress):
        """
        returns self.YieldStrength / appliedStress  
        Requires self.SetYieldStrength(yieldStrength)
        """
        if not self.YieldStrength:
            return None
        elif appliedStress == 0:
            return None
        else:
            return self.YieldStrength / appliedStress
    

    def getAvgStress(self):
        return (self.SigmaX + self.SigmaY + self.SigmaZ) / 3
    

    def getFailureAnalysis(self, analysis="MSS"):
        """  
        Ductile Materials:
            "MSS" - maximum shear stress theory
            "DE"  - distortion energy theory
        """

        if analysis == "MSS":
            # Mohr circle maximization, uses principle stresses
            t1 = (self.Sigma1 - self.Sigma2)
            t2 = (self.Sigma2 - self.Sigma3)
            t3 = (self.Sigma1 - self.Sigma3)
            shears = [t1, t2, t3]
            vm = max(shears)

            print(f"\nMaximm Shear Stress Theory")
            print(f"Shears:         {shears}")
            print(f"Max Stress:     {vm}")
            print(f"FOS:            {self.getFos(vm)}")
        
        elif analysis == "DE":
            # plug into 3d von mises formula
            stresses = (self.SigmaX - self.SigmaY)**2 + (self.SigmaY - self.SigmaZ)**2 + (self.SigmaZ - self.SigmaX)**2
            shears = (self.ShearXY**2 + self.ShearYZ**2 + self.ShearZX**2)
            de = (1/(2**.5))*(stresses + 6 * shears)**.5
            
            print(f"\nDistortion Energy Theory")
            print(f"Max Stress:     {de}")
            print(f"FOS:            {self.getFos(de)}")
        
        else:
            raise Exception(f"No analysis named {analysis}")


if __name__ == "__main__":
    Se = StressElement(-30, -65, 0, shearXY=40)
    Se.setYieldStrength(295)

    Se.getFailureAnalysis("MSS")
    Se.getFailureAnalysis("DE")
