from beam_analysis.utils import getAbsMax


class Test_Utils_getAbsMax:
    def test_utils_single(self):
        expected = 1
        single = [expected]
        
        result = getAbsMax(single)
        test = result == expected
        
        assert test
    
    def test_utils_uniform(self):
        expected = 1
        uniform = []
        
        for _i in range(10):
            uniform.append(expected)
        
        result = getAbsMax(uniform)
        test = result == expected
        
        assert test
    
    def test_utils_positive(self):
        expected = 10
        uniform = [1, 2, 3, expected, 4]
        
        result = getAbsMax(uniform)
        test = result == expected
        
        assert test
    
    def test_utils_negative(self):
        expected = 10
        uniform = [-1, -2, -3, -expected, -4]
        
        result = getAbsMax(uniform)
        test = result == expected
        
        assert test