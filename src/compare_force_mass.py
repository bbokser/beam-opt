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
    density = mat["density"]
    SF = 2
    thickness_min = mat["thickness_min"]
    g = 9.81
    Lx = 0.3
    Ly = 0.05
    def_max = 1 # 0.001
    R0 = 0.03  # initial guess for R

    m = 80
    for j in range(N):
        P = m * g * SF
        R, r = opt(material=mat, def_max=def_max, thickness_min=thickness_min, P=P, Lx=Lx, Ly=Ly, R0=R0)
        A = np.pi * (R**2 - r**2)
        Vol = A * Lx
        force[i, j] = m * g  # don't use SF for this
        mass[i, j] = Vol * density  # mass of the beam
        m += 1
# print(force)
# print(mass)
plots.plot_fit(force, mass, ["titanium", "cfrp", "aluminum"], "Applied Force (N)", "Required Beam Mass (kg)")
    
