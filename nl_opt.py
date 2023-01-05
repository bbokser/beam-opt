import nlopt
import numpy as np
import sigfig

# material = 'titanium'
material = 'cfrp'
# material = 'aluminum'

print("Using material = ", material)

if material == 'titanium':
    # Annealed Grade 5 Titanium
    # https://www.makeitfrom.com/material-properties/Annealed-Grade-5-Titanium
    E = 110e9  # Pa
    shear_str = 600e6  # Pa
    yield_str = 910e6  # Pa
    density = 4430  # g/cc -> kg/m3
    SF = 2  # safety factor
    min_thickness = 0.0004064  # 0.016" = 0.4064 mm

elif material == 'cfrp':
    # CFRP Tube from Dragonplate, 0/90
    # e.g. https://dragonplate.com/carbon-fiber-roll-wrapped-twill-tube-2-id-x-96-thin-wall-gloss-finish
    # http://www.performance-composites.com/carbonfibre/mechanicalproperties_2.asp
    E = 5.171059e11
    shear_str = 90e6
    yield_str = 600e6  # Pa  # actually just UTS
    density = 1522  # kg/m3
    SF = 4  # safety factor
    min_thickness = 0.000762

elif material == 'aluminum':
    # Aluminum 7075-T6
    # https://www.makeitfrom.com/material-properties/7075-T6-Aluminum
    E = 70e9
    shear_str = 330e6
    yield_str = 480e6  # Pa  # actually just UTS
    density = 2710  # kg/m3
    SF = 2  # safety factor
    min_thickness = 0.0004064  # 0.016" = 0.4064 mm

else:
    raise Exception("Invalid material choice")

m_ee = 3  # kg assumed mass of end effector
L_ee = 0.05  # assumed length of gripper

m_weight = 20  # kg
m = m_ee + m_weight  # kg
g = 9.81
L = 0.25
def_max = 0.0005 * 0.95  # mm

P = m * g * SF
M = P * L  # moment
torque = P * L_ee  # moment due to end effector

def objfunc(x, grad):
    if grad.size > 0:
        grad[0] = 2 * x[0]  # partial derivatives
        grad[1] = - 2 * x[1]
    return x[0]**2 - x[1]**2

# def shear_constr(x, grad):
#     if grad.size > 0:
#         grad[0] = shear_str * np.pi * 2 * x[0]
#         grad[1] = -shear_str * np.pi * 2 * x[1]
#     return 2 * P  - shear_str * np.pi * (x[0]**2 - x[1]**2)

def shear_constr(x, grad):
    if grad.size > 0:
        grad[0] = np.pi * torque * x[0] * (2 * x[0]**2 + (x[0]**2 - x[1]**2)) + \
            4 * x[0]**3 * P * np.pi + \
            - np.pi**2 * shear_str * (2 * x[0]**3 * (x[0]**2 - x[1]**2) - x[0] * (x[0]**4 - x[1]**4))
        grad[1] = - 2 * torque * x[0] * x[1] * np.pi * 2 + \
            - 8 * x[1]**3 * P + \
            - np.pi**2 * x[1]**2 * shear_str * (2 * x[1] * (x[0]**2 - x[1]**2) + (x[0]**4 - x[1]**4))
    return torque * x[0] * np.pi * (x[0]**2 - x[1]**2)  + P * np.pi * (x[0]**4 - x[1]**4) - shear_str * np.pi**2 * (x[0]**4 - x[1]**4) * (x[0]**2 - x[1]**2)

def tensile_constr(x, grad):
    if grad.size > 0:
        grad[0] = 4 * M - yield_str * np.pi * 4 * x[0]**3
        grad[1] = yield_str * np.pi * 4 * x[1]**3
    return 4 * M * x[0] - yield_str * np.pi * (x[0]**4 - x[1]**4)

def def_constr(x, grad):
    if grad.size > 0:
        grad[0] = -def_max * 12 * E * np.pi * x[0]**3 
        grad[1] = def_max * 12 * E * np.pi * x[1]**3
    return 4 * P * L**3 - def_max * 3 * E * np.pi * (x[0]**4 - x[1]**4)

def thickness_constr(x, grad):
    if grad.size > 0:
        grad[0] = -1
        grad[1] = 1
    return -x[0] + x[1] + min_thickness

opt = nlopt.opt(nlopt.LD_MMA, 2)
opt.set_lower_bounds([0.010, 0.010])
opt.set_upper_bounds([0.075, 0.075])
opt.set_min_objective(objfunc)
opt.add_inequality_constraint(lambda x, grad:shear_constr(x, grad), 1e-8)
opt.add_inequality_constraint(lambda x, grad:tensile_constr(x, grad), 1e-8)
opt.add_inequality_constraint(lambda x, grad:thickness_constr(x, grad), 1e-8)
opt.add_inequality_constraint(lambda x, grad:def_constr(x, grad), 1e-8)
opt.set_xtol_rel(1e-6)
# x = opt.optimize([0.019, 0.018])
x = opt.optimize([0.029, 0.028])
minf = opt.last_optimum_value()
print("optimum at ", x[0], ", ", x[1])
print("minimum value = ", minf)
print("result code = ", opt.last_optimize_result())
print("\n")

# --- check --- #
R = x[0]
r = x[1]

I = np.pi * (R**4 - r**4)/4
print("Second Moment of Area = ", I, " m^4")

assert R > r
print("R = ", R, " m")
print("r = ", r, " m")

A = np.pi * (R**2 - r**2)
print("Cross-Sectional Area = ", A, " m^2")
print("\n")

M_max = P * L
max_tensile_stress = M_max * R / I
assert yield_str > max_tensile_stress
print("Maximum tensile stress = ", max_tensile_stress, " Pa")
print("Tensile Stress / Yield Strength = ", max_tensile_stress/yield_str)
print("\n")

# shear stress check
max_shear_stress = 2 * P / A
print("Shear stress due to downward force, max = ", max_shear_stress, " Pa")

# torsion check
J = np.pi * (R**4 - r**4) / 2  # polar moment of inertia
shear_torsional = torque * R / J
print("Torsional shear = ", shear_torsional, " Pa")

max_shear_stress_total = max_shear_stress + shear_torsional
print("Total max shear = ", max_shear_stress_total, " Pa")
assert shear_str >= max_shear_stress_total
print("Shear stress / Shear Strength = ", max_shear_stress_total/shear_str)
print("\n")

# deflection check
deflection = P * L**3 / (3 * E * I)
# assert sigfig.round(def_max, 3) > sigfig.round(deflection, 3)
print("Deflection = ", deflection * 1000, " mm")
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