import numpy as np

from beam_opt_radius_const import opt_r
from check_calc import check
import materials
import plots

n = 3  # number of materials
mass = np.zeros(n)
th = np.zeros(n)
radius = np.zeros(n)

mat_list = [materials.titanium, materials.cfrp, materials.aluminum]
mat_str = ["titanium", "cfrp", "aluminum"]

g = 9.81
Lx = 0.3
Ly = 0.05
def_max = 0.0005
m = 80
R0 = 0.03  # initial guess for R

for i in range(n):
    mat = mat_list[i]
    E = mat["E"]
    shear_str = mat["shear_str"]
    yield_str = mat["yield_str"]
    density = mat["density"]
    SF = mat["SF"]
    thickness_min = mat["thickness_min"]

    print("Using material: ", mat_str[i])

    P = m * g * SF
    r = opt_r(material=mat, def_max=def_max, thickness_min=thickness_min, P=P, Lx=Lx, Ly=Ly, R0=R0)
    A = np.pi * (R0**2 - r**2)
    Vol = A * Lx
    radius[i] = r * 1000
    th[i] = (R0 - r) * 1000
    mass[i] = Vol * density  # mass of the beam
    check(material=mat, def_max=def_max, P=P, Lx=Lx, Ly=Ly, R=R0, r=r)

print("Using a constant outer radius of ", R0 * 1000, "mm :")
print("material: ", mat_str)
print("inner r: ", radius)
print("thickness: ", th)
print("mass: ", mass)
# plots.bar(th, ["titanium", "cfrp", "aluminum"], "Wall Thickness (mm)")
# plots.bar(mass, ["titanium", "cfrp", "aluminum"], "Required Beam Mass (kg)")
    
