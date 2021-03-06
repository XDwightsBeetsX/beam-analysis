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
        return "{:>9} {:<6} @ {:>6} [m]".format(f"{self.Value:.4f}", self.Units, round(self.Point, 3))
