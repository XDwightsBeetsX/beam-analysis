"""
BEAM-ANALYSIS

1. Define Beam Parameters
2. Add Loads
3. Input Boundary Conditions
4. Run Analysis
"""

from beam_analysis.Beam import Beam
from beam_analysis.utils import PREFIX

if __name__ == "__main__":
    print(f"{PREFIX} running...")    
    # =============================== #
    # ======= Youngs Modulus E ====== #
    # ===== Moment of Inertia I ===== #
    # ======== Beam Length L ======== #
    # =============================== #
    E = 207 * 10**9
    I = 2 * 10**-8
    
    a = 2
    b = 1
    L = 2*a + b
    w = 100
    P = 1000

    # =============================== #
    # = Make the beam and add loads = #
    # =============================== #
    B = Beam(L, E, I)
    
    B.addDistributedLoad(0, a, -w)
    B.addPointLoad(a+b/2, -P)
    B.addDistributedLoad(a+b, L, -w)

    rb = (1/L)*(w*a*(2*a+b)+P*(a+b/2))
    ra = rb
    B.addPointLoad(0, ra)
    B.addPointLoad(L, rb)

    # =============================== #
    # === Add Boundary Conditions === #
    # =============================== #
    # currently req 1 to be angle and other to be deflection
    B.addBoundaryCondition(L/2, "angle", 0.0)
    B.addBoundaryCondition(0.0, "deflection", 0.0)

    # =============================== #
    # ======== Display Info ========= #
    # =============================== #
    B.showParams()

    # =============================== #
    # ======== Run Analysis ========= #
    # =============================== #
    B.analyze()
