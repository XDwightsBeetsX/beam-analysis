"""
PointValuePair class used for maximum values in Beam
"""


class PointValuePair(object):
    """
    Stores a point and value.  
    Offers a show() method
    """
    def __init__(self, point, value, units):
        self.Point = point
        self.Value = value
        self.Units = units
    
    def getString(self):
        """
        '[value][units] @ [point]m'
        """
        return f"{self.Value:.4f}{self.Units} @ {self.Point:.4f}m"
