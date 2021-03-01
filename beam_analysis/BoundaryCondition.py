

from .utils import ANGLE, DEFLECTION


class BoundaryCondition(object):
    """
    Stores a Boundary Condition
    location  
    bc_type  
    bc_value
    """
    def __init__(self, loc, bc_type=DEFLECTION, bc_value=0.0):
        self.Location = loc
        self.Bc_type = bc_type
        self.Bc_value = bc_value
