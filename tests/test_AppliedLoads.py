from beam_analysis.AppliedLoad import PointLoad, DistributedLoad, Moment
from beam_analysis.BeamAnalysisTypes import BeamAnalysisTypes


class Test_PointLoad:
    def test_PointLoad_Shear(self):
        loc = .5
        mag = 10
        pl = PointLoad(loc, mag)
        
        expected = mag
        result = pl.evaluateAt(.5, BeamAnalysisTypes.SHEAR)
        
        tol = 1E-10
        test = abs(result - expected) < tol
        
        assert test
    
    def test_PointLoad_Moment(self):
        loc = 0
        mag = 10
        pl = PointLoad(loc, mag)
        
        x = 2
        expected = mag * (x - loc)
        result = pl.evaluateAt(x, BeamAnalysisTypes.BENDING)
        
        tol = 1E-10
        test = abs(result - expected) < tol
        
        assert test


class Test_DistributedLoad:
    def test_DistributedLoad_Shear(self):
        start, stop = 0, 1
        mag = 5
        pl = DistributedLoad(start, stop, mag)
        
        x = 2
        expected = mag
        result = pl.evaluateAt(x, BeamAnalysisTypes.SHEAR)
        
        tol = 1E-10
        test = abs(result - expected) < tol
        
        assert test
