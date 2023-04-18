import numpy as np

from beam_opt import opt
import materials
import plots

n = 3  # number of materials
N = 20  # range
axial_offset = np.zeros((n, N))
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
    Lx = 0.3
    # Ly = 0.05
    def_max = 0.001
    m = 10
    R0 = 0.04  # initial guess for R

    for j in range(N):
        P = m * g * SF
        Ly = 0.01 + j * 0.05
        R, r = opt(material=mat, def_max=def_max, thickness_min=thickness_min, P=P, Lx=Lx, Ly=Ly, R0=R0)
        A = np.pi * (R**2 - r**2)
        Vol = A * Lx
        axial_offset[i, j] = Ly
        mass[i, j] = Vol * density  # mass of the beam
# print(force)
# print(mass)
# plots.plot_gen(axial_offset, mass, ["titanium", "cfrp", "aluminum"], "Axial Offset Ly (m)", "Required Beam Mass (kg)")
plots.plot_fit(axial_offset, mass, ["titanium", "cfrp", "aluminum"], "Axial Offset Ly (m)", "Required Beam Mass (kg)")
    
