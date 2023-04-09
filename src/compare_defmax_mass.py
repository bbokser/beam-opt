import numpy as np

from beam_opt import opt
import materials
import plots

# What should be tested:
# 1. Force vs Beam Mass
# 2. Axial Offset vs Beam Mass
# 3. Shear Force vs Beam Mass
# 4. Minimum Thickness vs Diameter
# 5. Max deflection vs Beam Mass

n = 3  # number of materials
N = 20  # range
deflection_max = np.zeros((n, N))
mass = np.zeros((n, N))
mat_list = [materials.titanium, materials.cfrp, materials.aluminum]

for i in range(n):
    mat = mat_list[i]
    E = mat["E"]
    shear_str = mat["shear_str"]
    yield_str = mat["yield_str"]
    density = mat["density"]
    SF = mat["SF"]
    thickness_min = mat["thickness_min"]
    g = 9.81
    Lx = 0.25
    Ly = 0.05
    def_max = 0.0005
    m = 20

    for j in range(N):
        P = m * g * SF
        def_max = 0.0005 + j * 0.0005
        Mx = P * Lx  # moment acting on beam lengthwise
        My = P * Ly  # axial moment due to end effector
        R, r = opt(material=mat, Lx=Lx, def_max=def_max, thickness_min=thickness_min, P=P, Mx=Mx, My=My)
        A = np.pi * (R**2 - r**2)
        Vol = A * Lx
        deflection_max[i, j] = def_max
        mass[i, j] = Vol * density  # mass of the beam
# print(force)
# print(mass)
plots.plot_gen(deflection_max, mass, ["titanium", "cfrp", "aluminum"], "Required Max Deflection (m)")
    
