import nlopt
import numpy as np

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

elif material == 'cfrp':
    # CFRP Tube from Dragonplate, 0/90
    # e.g. https://dragonplate.com/carbon-fiber-roll-wrapped-twill-tube-2-id-x-96-thin-wall-gloss-finish
    # http://www.performance-composites.com/carbonfibre/mechanicalproperties_2.asp
    E = 5.171059e11
    shear_str = 90e6
    yield_str = 600e6  # Pa  # actually just UTS
    density = 1522  # kg/m3
    SF = 4  # safety factor

elif material == 'aluminum':
    # Aluminum 7075-T6
    # https://www.makeitfrom.com/material-properties/7075-T6-Aluminum
    E = 70e9
    shear_str = 330e6
    yield_str = 480e6  # Pa  # actually just UTS
    density = 2710  # kg/m3
    SF = 2  # safety factor

else:
    raise Exception("Invalid material choice")

m = 20  # kg
g = 9.81
L = 0.25
def_max = 0.0005  # mm

P = m * g * SF
M = P * L

min_thickness = 0.0005

def objfunc(x, grad):
    if grad.size > 0:
        grad[0] = 2 * x[0]  # partial derivatives
        grad[1] = - 2 * x[1]
    return x[0]**2 - x[1]**2

def shear_constr(x, grad):
    if grad.size > 0:
        grad[0] = shear_str * np.pi * 2 * x[0]
        grad[1] = -shear_str * np.pi * 2 * x[1]
    return 2 * P  - shear_str * np.pi * (x[0]**2 - x[1]**2)

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
opt.set_lower_bounds([0.05, 0.05])
opt.set_upper_bounds([0.15, 0.15])
opt.set_min_objective(objfunc)
opt.add_inequality_constraint(lambda x, grad:shear_constr(x, grad), 1e-8)
opt.add_inequality_constraint(lambda x, grad:tensile_constr(x, grad), 1e-8)
opt.add_inequality_constraint(lambda x, grad:thickness_constr(x, grad), 1e-8)
opt.add_inequality_constraint(lambda x, grad:def_constr(x, grad), 1e-8)
opt.set_xtol_rel(1e-6)
x = opt.optimize([0.06, 0.057])
minf = opt.last_optimum_value()
print("optimum at ", x[0], ", ", x[1])
print("minimum value = ", minf)
print("result code = ", opt.last_optimize_result())

# --- check --- #
R = x[0]
r = x[1]

I = np.pi * (R**4 - r**4)/4
print("Moment of Inertia = ", I)

A = np.pi * (R**2 - r**2)
assert R > r
print("R = ", R)
print("r = ", r)
print("Cross-Sectional Area = ", A)

M_max = P * L
max_tensile_stress = M_max * R / I
assert yield_str > max_tensile_stress
print("Maximum tensile stress = ", max_tensile_stress)
print("Yield Strength exceeded by factor of ", max_tensile_stress/yield_str)

max_shear_stress = 2 * P / A
assert shear_str > max_shear_stress
# assert sigfig.round(shear_str, 4) == sigfig.round(max_shear_stress, 4)
print("Maximum shear stress = ", max_shear_stress)
print("Shear strength exceeded by factor of ", max_shear_stress/shear_str)

# deflection check
deflection = P * L**3 / (3 * E * I)
assert def_max > deflection
print("Deflection = ", deflection * 1000, " mm")
print("Deflection limit exceeded by factor of ", deflection/def_max)

print("Thickness = ", (R - r)*1000, " mm")

Vol = A * L
m_beam = Vol * density
print("Mass of the beam = ", m_beam, " kg")