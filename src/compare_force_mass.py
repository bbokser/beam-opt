import numpy as np

from beam_opt import opt
import materials
import plots

n = 3  # number of materials
N = 20  # range
force = np.zeros((n, N))
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
    Lx = 3
    Ly = 0.1
    def_max = 3

    m = 0
    for j in range(N):
        P = m * g * SF
        R, r = opt(material=mat, def_max=def_max, thickness_min=thickness_min, P=P, Lx=Lx, Ly=Ly)
        A = np.pi * (R**2 - r**2)
        Vol = A * Lx
        force[i, j] = m * g  # don't use SF for this
        mass[i, j] = Vol * density  # mass of the beam
        m += 6
# print(force)
# print(mass)
plots.plot_fit(force, mass, ["titanium", "cfrp", "aluminum"], "Applied Force (N)", "Required Beam Mass (kg)")
    
