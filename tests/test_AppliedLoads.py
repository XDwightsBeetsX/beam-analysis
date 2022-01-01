from beam_analysis.AppliedLoad import PointLoad, DistributedLoad, Moment
from beam_analysis.BeamAnalysisTypes import BeamAnalysisTypes


class Test_PointLoad:
    def test_Shear_Analysis(self):
        loc = .5
        mag = 10
        pl = PointLoad(loc, mag)
        
        x = loc
        result = pl.evaluateAt(x, BeamAnalysisTypes.SHEAR)
        expected = mag

        tol = 1E-10
        test = abs(result - expected) < tol
        
        assert test
    
    def test_Bending_Analysis(self):
        loc = 0
        mag = 10
        pl = PointLoad(loc, mag)
        
        x = 2
        result = pl.evaluateAt(x, BeamAnalysisTypes.BENDING)
        expected = mag * (x - loc)

        tol = 1E-10
        test = abs(result - expected) < tol
        
        assert test
    
    def test_Angle_Analysis(self):
        loc = 0
        mag = 10
        pl = PointLoad(loc, mag)
        
        x = 2
        result = pl.evaluateAt(x, BeamAnalysisTypes.ANGLE)
        expected = (mag / 2) * (x - loc)**2

        tol = 1E-10
        test = abs(result - expected) < tol
        
        assert test
    
    def test_Deflection_Analysis(self):
        loc = 0
        mag = 10
        pl = PointLoad(loc, mag)
        
        x = 2
        result = pl.evaluateAt(x, BeamAnalysisTypes.DEFLECTION)
        expected = (mag / 6) * (x - loc)**3

        tol = 1E-10
        test = abs(result - expected) < tol
        
        assert test


class Test_DistributedLoad:
    def test_Shear_Analysis(self):
        start, stop = 0, 3
        mag = 5
        dl = DistributedLoad(start, stop, mag)
        
        x = 2
        result = dl.evaluateAt(x, BeamAnalysisTypes.SHEAR)
        expected = mag * (x - start)

        tol = 1E-10
        test = abs(result - expected) < tol
        
        assert test
    
    def test_Bending_Analysis(self):
        start, stop = 0, 3
        mag = 5
        dl = DistributedLoad(start, stop, mag)
        
        x = 3
        result = dl.evaluateAt(x, BeamAnalysisTypes.BENDING)
        expected = (mag / 2) * (x - start)**2

        tol = 1E-10
        test = abs(result - expected) < tol
        
        print(expected, result)
        assert test
    
    def test_Angle_Analysis(self):
        start, stop = 0, 3
        mag = 5
        dl = DistributedLoad(start, stop, mag)
        
        x = 2
        result = dl.evaluateAt(x, BeamAnalysisTypes.ANGLE)
        expected = (mag / 6) * (x - start)**3

        tol = 1E-10
        test = abs(result - expected) < tol
        
        assert test
    
    def test_Deflection_Analysis(self):
        start, stop = 0, 3
        mag = 5
        dl = DistributedLoad(start, stop, mag)
        
        x = 2
        result = dl.evaluateAt(x, BeamAnalysisTypes.DEFLECTION)
        expected = (mag / 24) * (x - start)**4

        tol = 1E-10
        test = abs(result - expected) < tol
        
        assert test


class Test_Moment:
    def test_Shear_Analysis(self):
        loc = 0
        mag = 5
        m = Moment(loc, mag)
        
        x = 2
        result = m.evaluateAt(x, BeamAnalysisTypes.SHEAR)
        expected = 0.0

        test = result == expected
        
        assert test
    
    def test_Bending_Analysis(self):
        loc = 0
        mag = 5
        m = Moment(loc, mag)
        
        x = 3
        result = m.evaluateAt(x, BeamAnalysisTypes.BENDING)
        expected = mag

        test = result == expected
        
        assert test

    def test_Angle_Analysis(self):
        loc = 0
        mag = 5
        m = Moment(loc, mag)
        
        x = 3
        result = m.evaluateAt(x, BeamAnalysisTypes.ANGLE)
        expected = mag * (x - loc)
        
        test = result == expected
        
        assert test
    
    def test_Deflection_Analysis(self):
        loc = 0
        mag = 5
        m = Moment(loc, mag)
        
        x = 3
        result = m.evaluateAt(x, BeamAnalysisTypes.DEFLECTION)
        expected = (mag / 2) * (x - loc)**2
        
        test = result == expected
        
        assert test
