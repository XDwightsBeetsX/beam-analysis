"""
BEAM-ANALYSIS

1. Define Beam Parameters
2. Add Loads
3. Input Boundary Conditions
4. Run Analysis
"""

from beam_analysis.Beam import Beam
from beam_analysis.BoundaryCondition import BoundaryConditionTypes
from beam_analysis.CrossSection import CrossSection, CrossSectionTypes


if __name__ == "__main__":
    # =================================== #
    #    1. Define Beam Parameters        #
    # =================================== #
    # E - Youngs Modulus                  #
    # I - Moment of Inertia I             #
    # L - Beam Length                     #
    # =================================== #
    E = 207 * 10**9
    L = 1.0
    CS = CrossSection(CrossSectionTypes.CIRC, [.01])
    B = Beam(L, E, crossSection=CS)


    # =================================== #
    #    2. Add Loads                     #
    # =================================== #
    # Use theta = 0 to indicate XY plane  #
    # Use theta = 90 to indicate XZ plane #
    #                                     #
    #           | (90 - XZ plane)         #
    #        \  |                         #
    #         \ |                         #
    #          \|________ (0 - XY plane)  #
    # =================================== #
    B.addPointLoad(0, 10, 0)
    B.addPointLoad(0, 10, 90)

    B.addPointLoad(L/2, -20, 0)
    B.addPointLoad(L/2, -20, 90)

    B.addPointLoad(L, 10, 0)
    B.addPointLoad(L, 10, 90)

    # =================================== #
    #    3. Input Boundary Conditions     #
    # =================================== #
    # Use the loading angle convention    #
    # =================================== #
    # B.addBoundaryCondition(L/2, BoundaryConditionTypes.ANGLE, 0)
    B.addBoundaryCondition(0, BoundaryConditionTypes.DEFLECTION, 0)
    B.addBoundaryCondition(L, BoundaryConditionTypes.DEFLECTION, 0.0)


    # =================================== #
    #    4. Run Analysis                  #
    # =================================== #
    B.runAnalysis()
