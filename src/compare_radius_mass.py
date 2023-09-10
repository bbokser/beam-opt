import numpy as np

from beam_opt_radius_const import opt_r
import materials
import plots

n = 3  # number of materials
N = 20  # range
mass = np.zeros((n, N))
th = np.zeros((n, N))
radius = np.zeros((n, N))

mat_list = [materials.titanium, materials.cfrp, materials.aluminum]
mat_str = ["titanium", "cfrp", "aluminum"]

g = 9.81
Lx = 0.3
Ly = 0.05
def_max = 0.001
m = 30
SF = 2
P = m * g * SF

for i in range(n):
    mat = mat_list[i]
    density = mat["density"]
    thickness_min = mat["thickness_min"]

    print("Using material: ", mat_str[i])

    for j in range(N):
        R = 0.018 + j * 0.0005
        r0 = R - 0.006 + j * 0.0001
        r = opt_r(material=mat, def_max=def_max, thickness_min=thickness_min, P=P, Lx=Lx, Ly=Ly, R=R, r0=r0)
        A = np.pi * (R**2 - r**2)
        Vol = A * Lx
        radius[i, j] = R * 1000
        th[i, j] = (R - r) * 1000
        mass[i, j] = Vol * density  # mass of the beam

plots.plot_gen(radius, mass, ["titanium", "cfrp", "aluminum"], "Max Allowable Radius (mm)", "Required Beam Mass (kg)")
# plots.plot_fit(radius, mass, ["titanium", "cfrp", "aluminum"], "Max Allowable Radius (mm)", "Required Beam Mass (kg)")
    
