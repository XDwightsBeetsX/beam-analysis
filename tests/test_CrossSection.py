import numpy as np

from beam_analysis.CrossSection import CrossSection, CrossSectionTypes


class Test_CrossSection_getArea:
    def test_CrossSection__getArea_RECT(self):
        w = 2
        h = 3
        CS = CrossSection(CrossSectionTypes.RECT, dims=[w, h])
        
        expected = w * h
        result = CS.getArea()
        test = result == expected
        
        assert test
    
    def test_CrossSection_getArea_CIRC(self):
        r = 2
        CS = CrossSection(CrossSectionTypes.CIRC, dims=[r])
        
        expected = np.pi * r**2
        result = CS.getArea()

        tol = 1E-10
        test = abs(result - expected) < tol
        
        assert test


class Test_CrossSection_getInertia:
    def test_CrossSection__getInertia_RECT(self):
        w = 2
        h = 3
        CS = CrossSection(CrossSectionTypes.RECT, dims=[w, h])
        
        expected = w * h**3 / 12
        result = CS.getI()
        
        tol = 1E-10
        test = abs(result - expected) < tol
        
        assert test
    
    def test_CrossSection__getInertia_CIRC(self):
        r = 2
        CS = CrossSection(CrossSectionTypes.CIRC, dims=[r])
        
        expected = (np.pi / 4) * r**4
        result = CS.getI()

        tol = 1E-10
        test = abs(result - expected) < tol
        
        assert test
