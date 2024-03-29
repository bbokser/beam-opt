import numpy as np

from beam_opt import opt
import materials
import plots

n = 3  # number of materials
N = 20  # range
thmin = np.zeros((n, N))
mass = np.zeros((n, N))
mat_list = [materials.titanium, materials.cfrp, materials.aluminum]
g = 9.81
Lx = 0.25
Ly = 0.05
def_max = 0.0005
m = 20
R0 = 0.02  # initial guess for R
SF = 2
P = m * g * SF

for i in range(n):
    mat = mat_list[i]
    density = mat["density"]
    
    for j in range(N):
        thickness_min = 0.0005 + j * 0.0005
        R, r = opt(material=mat, def_max=def_max, thickness_min=thickness_min, P=P, Lx=Lx, Ly=Ly, R0=R0)
        A = np.pi * (R**2 - r**2)
        Vol = A * Lx
        thmin[i, j] = thickness_min
        mass[i, j] = Vol * density  # mass of the beam
# print(force)
# print(mass)
plots.plot_gen(thmin, mass, ["titanium", "cfrp", "aluminum"], "Minimum Allowed Wall Thickness (m)", "Required Beam Mass (kg)")
    
