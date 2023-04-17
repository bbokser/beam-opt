import numpy as np

from beam_opt import opt
import materials
import plots

n = 3  # number of materials
N = 20  # range
thmin = np.zeros((n, N))
mass = np.zeros((n, N))
mat_list = [materials.titanium, materials.cfrp, materials.aluminum]

for i in range(n):
    mat = mat_list[i]
    E = mat["E"]
    shear_str = mat["shear_str"]
    yield_str = mat["yield_str"]
    density = mat["density"]
    SF = mat["SF"]
    # thickness_min = mat["thickness_min"]
    g = 9.81
    Lx = 0.25
    Ly = 0.05
    def_max = 0.0005
    m = 20

    for j in range(N):
        P = m * g * SF
        thickness_min = 0.0005 + j * 0.001
        Mx = P * Lx  # moment acting on beam lengthwise
        My = P * Ly  # axial moment due to end effector
        R, r = opt(material=mat, Lx=Lx, def_max=def_max, thickness_min=thickness_min, P=P, Mx=Mx, My=My)
        A = np.pi * (R**2 - r**2)
        Vol = A * Lx
        thmin[i, j] = thickness_min
        mass[i, j] = Vol * density  # mass of the beam
# print(force)
# print(mass)
plots.plot_gen(thmin, mass, ["titanium", "cfrp", "aluminum"], "Minimum Allowed Wall Thickness (m)", "Required Beam Mass (kg)")
    
