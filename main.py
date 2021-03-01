"""
BEAM-ANALYSIS
"""

from beam_analysis.Beam import Beam

if __name__ == "__main__":
    print("running...")
    
    # =============================== #
    # ======= Youngs Modulus E ====== #
    # ===== Moment of Inertia I ===== #
    # ======== Beam Length L ======== #
    # =============================== #
    E = 207 * 10**9
    I = 2 * 10**-8
    L = 1.0

    # =============================== #
    # = Make the beam and add loads = #
    # =============================== #
    B = Beam(L, E, I)
    B.addPointLoad(0, 11)
    B.addPointLoad(1, 11)
    B.addPointLoad(.5, -20)
    B.addDistributedLoad(0, 1, -2)

    # =============================== #
    # = Make the beam and add loads = #
    # =============================== #


    # =============================== #
    # ======== Display Info ========= #
    # =============================== #
    B.showParams()
    # B.showForcesAndMoments()   
    
    # =============================== #
    # ======== Run Analysis ========= #
    # =============================== #
    B.analyze()