"""
BEAM-ANALYSIS

1. Define Beam Parameters
2. Add Loads
3. Input Boundary Conditions
4. Run Analysis
"""

from beam_analysis.Beam import Beam
from beam_analysis.Enums import Planes, BoundaryConditionTypes


if __name__ == "__main__":
    # =================================== #
    #    1. Define Beam Parameters        #
    # =================================== #
    #    E - Youngs Modulus               #
    #    I - Moment of Inertia I          #
    #    L - Beam Length                  #
    # =================================== #
    E = 207 * 10**9
    I = 2 * 10**-8
    L = 4
    
    B = Beam(L, E, I)


    # =================================== #
    #    2. Add Loads                     #
    # =================================== #
    # B.addDistributedLoad(0, L, -1000, Planes.XY)
    B.addPointLoad(L/2, -10000, Planes.XY)
    B.addPointLoad(0, 10000/2, Planes.XY)
    B.addPointLoad(L, 10000/2, Planes.XY)


    # =================================== #
    #    3. Input Boundary Conditions     #
    # =================================== #
    # TODO currently req 1 to be angle and other to be deflection
    B.addBoundaryCondition(L/2, BoundaryConditionTypes.ANGLE, 0.0, Planes.XY)
    B.addBoundaryCondition(0.0, BoundaryConditionTypes.DEFLECTION, 0.0, Planes.XY)


    # =================================== #
    #    4. Run Analysis                  #
    # =================================== #
    B.runAnalysis()
