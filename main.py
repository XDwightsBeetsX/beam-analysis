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
    B.addPointLoad(0, 10)
    B.addPointLoad(1, 10)
    B.addPointLoad(.5, -20)

    # =============================== #
    # ========== Parameters ========= #
    # =============================== #
    B.showParams()
    
    # =============================== #
    # ========= Added loads ========= #
    # =============================== #
    # B.showForcesAndMoments()
    
    # =============================== #
    # ==== Run Forrest Run!! ======== #
    # =============================== #
    B.analyze()