import numpy as np

from beam_opt import opt
import materials
import plots

n = 3  # number of materials
N = 20  # range
deflection_max = np.zeros((n, N))
mass = np.zeros((n, N))
mat_list = [materials.titanium, materials.cfrp, materials.aluminum]
g = 9.81
Lx = 0.3
Ly = 0.005
def_max = 0.0005
m = 30
R0 = 0.018  # initial guess for R
SF = 2
P = m * g * SF

for i in range(n):
    mat = mat_list[i]
    density = mat["density"]
    thickness_min = mat["thickness_min"]
    for j in range(N):
        def_max = 0.0005 + j * 0.001
        R, r = opt(material=mat, def_max=def_max, thickness_min=thickness_min, P=P, Lx=Lx, Ly=Ly, R0=R0)
        A = np.pi * (R**2 - r**2)
        Vol = A * Lx
        deflection_max[i, j] = def_max
        mass[i, j] = Vol * density  # mass of the beam
# print(force)
# print(mass)
plots.plot_gen(deflection_max, mass, ["titanium", "cfrp", "aluminum"], "Required Max Deflection (m)", "Required Beam Mass (kg)")
plots.plot_fit(deflection_max, mass, ["titanium", "cfrp", "aluminum"], "Required Max Deflection (m)", "Required Beam Mass (kg)")
    
