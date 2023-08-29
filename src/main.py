import argparse
import numpy as np

from beam_opt import opt
from check_calc import check
import materials

parser = argparse.ArgumentParser()

parser.add_argument("material", help="enter the material", choices=["titanium", "cfrp", "aluminum"], type=str, default="titanium")
parser.add_argument("mass", help="enter the mass at the end-effector", type=float, default=20.0)
parser.add_argument("Lx", help="enter the length of the beam", type=float, default=0.25)
parser.add_argument("Ly", help="enter the axial offset distance", type=float, default=0.05)
parser.add_argument("def_max", help="enter the maximum beam deflection allowed", type=float, default=0.0005)
parser.add_argument("thickness_min", help="enter the minimum wall thickness allowed", type=float, default=0.0004064)
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

E_flex = mat["E_flex"]
E_comp = mat["E_comp"]
shear_str = mat["shear_str"]
flex_str = mat["flex_str"]
density = mat["density"]
SF = 2

m = args.mass
Lx = args.Lx
Ly = args.Ly
def_max = args.def_max

g = 9.81
P = m * g * SF

R, r = opt(material=mat, def_max=def_max, thickness_min=args.thickness_min, P=P, Lx=Lx, Ly=Ly, R0=0.04)

check(material=mat, def_max=def_max, P=P, Lx=Lx, Ly=Ly, R=R, r=r)