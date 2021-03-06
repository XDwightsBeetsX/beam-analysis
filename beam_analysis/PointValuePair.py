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
        return "{:<8} {:<6} @ {:>6} [m]".format(round(self.Value, 5), self.Units, round(self.Point, 3))
