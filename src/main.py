import argparse
import numpy as np

from beam_opt import opt
import materials

parser = argparse.ArgumentParser()

parser.add_argument("material", help="enter the material", choices=["titanium", "cfrp", "aluminum"], type=str, default="titanium")
parser.add_argument("mass", help="enter the mass at the end-effector", type=float, default=20.0)
parser.add_argument("L_beam", help="enter the length of the beam", type=float, default=0.25)
parser.add_argument("L_ee", help="enter the length of the end-effector", type=float, default=0.05)
parser.add_argument("def_max", help="enter the maximum beam deflection allowed", type=float, default=0.0005)
args = parser.parse_args()

print("Using material = ", args.material)
if args.material=="titanium":
    mat = materials.titanium
elif args.material=="cfrp":
    mat = materials.cfrp
elif args.material=="aluminum":
    mat = materials.aluminum
else:
    raise Exception("Invalid material choice")

E = mat["E"]
shear_str = mat["shear_str"]
yield_str = mat["yield_str"]
density = mat["density"]
SF = mat["SF"]

m = args.mass
L = args.L_beam
L_ee = args.L_ee
def_max = args.def_max

g = 9.81
P = m * g * SF
M = P * L  # moment acting on beam lengthwise
M_axial = P * L_ee  # axial moment due to end effector

R, r = opt(material=mat, L=L, def_max=def_max, P=P, M=M, M_axial=M_axial)

assert R > r
print("R = ", R, " m")
print("r = ", r, " m")

I = np.pi * (R**4 - r**4)/4
print("Second Moment of Area = ", I, " m^4")

A = np.pi * (R**2 - r**2)
print("Cross-Sectional Area = ", A, " m^2")
print("\n")

M_max = P * L
max_tensile_stress = M_max * R / I
assert yield_str >= max_tensile_stress
print("Maximum tensile stress = ", max_tensile_stress, " Pa")
print("Tensile Stress / Yield Strength = ", max_tensile_stress/yield_str)
print("\n")

# shear stress check
max_shear_stress = 2 * P / A
print("Shear stress due to downward force, max = ", max_shear_stress, " Pa")

# torsion check
J = np.pi * (R**4 - r**4) / 2  # polar moment of inertia
shear_torsional = M_axial * R / J
print("Torsional shear = ", shear_torsional, " Pa")

max_shear_stress_total = max_shear_stress + shear_torsional
print("Total max shear = ", max_shear_stress_total, " Pa")
assert shear_str >= max_shear_stress_total
print("Shear stress / Shear Strength = ", max_shear_stress_total/shear_str)
print("\n")

# deflection check
deflection = P * L**3 / (3 * E * I)
print("Deflection = ", deflection * 1000, " mm")
assert (def_max + 0.00001) >= deflection
print("Deflection / Deflection Limit = ", deflection/def_max)
print("\n")

# buckling check
P_critical = np.pi**2 * E * I / (L**2)
assert P_critical >= P
print("Critical load for buckling = ", P_critical, " N")
print("Load / Critical Buckling Load Limit = ", P/P_critical)
print("\n")

print("Thickness = ", (R - r)*1000, " mm")

Vol = A * L
print("Total Volume = ", Vol, " m^3")
m_beam = Vol * density
print("Mass of the beam = ", m_beam, " kg")