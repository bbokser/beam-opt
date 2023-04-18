import numpy as np


def check(material, def_max, P, Lx, Ly, R, r):
    E = material["E"]
    shear_str = material["shear_str"]
    yield_str = material["yield_str"]
    density = material["density"]
    My = P * Lx
    Mx = P * Ly
    
    print("R = ", R, " m")
    print("r = ", r, " m")
    assert R > r

    I = np.pi * (R**4 - r**4)/4
    print("Second Moment of Area = ", I, " m^4")

    A = np.pi * (R**2 - r**2)
    print("Cross-Sectional Area = ", A, " m^2")
    print("\n")

    max_tensile_stress = My * R / I
    print("Maximum tensile stress = ", max_tensile_stress, " Pa")
    print("Tensile Stress / Yield Strength = ", max_tensile_stress/yield_str)
    assert yield_str >= max_tensile_stress - 500
    print("\n")

    # shear stress check
    max_shear_stress = 2 * P / A
    print("Shear stress due to downward force, max = ", max_shear_stress, " Pa")

    # torsion check
    J = np.pi * (R**4 - r**4) / 2  # polar moment of inertia
    shear_torsional = Mx * R / J
    print("Torsional shear = ", shear_torsional, " Pa")

    max_shear_stress_total = max_shear_stress + shear_torsional
    print("Total max shear = ", max_shear_stress_total, " Pa")
    print("Shear stress / Shear Strength = ", max_shear_stress_total/shear_str)
    assert shear_str >= max_shear_stress_total - 500  # accounting for numerical error...
    print("\n")

    # deflection check
    deflection = P * Lx**3 / (3 * E * I)
    print("Deflection = ", deflection * 1000, " mm")
    print("Deflection / Deflection Limit = ", deflection/def_max)
    assert (def_max + 0.00001) >= deflection
    print("\n")

    # buckling check
    P_critical = np.pi**2 * E * I / (Lx**2)
    print("Critical load for buckling = ", P_critical, " N")
    print("Load / Critical Buckling Load Limit = ", P/P_critical)
    assert P_critical >= P
    print("\n")

    print("Thickness = ", (R - r)*1000, " mm")

    Vol = A * Lx
    print("Total Volume = ", Vol, " m^3")
    m_beam = Vol * density
    print("Mass of the beam = ", m_beam, " kg")

    print("\n")

    return 1


