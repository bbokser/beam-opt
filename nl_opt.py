import nlopt
import numpy as np

E = 110e9  # Pa
shear_str = 600e6  # Pa
yield_str = 910e6  # Pa
density = 4.43 * 1000  # g/cc -> kg/m3
m = 20  # kg
SF = 2  # safety factor
g = 9.81
L = 0.25
def_max = 0.0005  # mm

P = m * g * SF
M = P * L

min_thickness = 0.002

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
opt.set_xtol_rel(1e-6)
x = opt.optimize([0.1, 0.098])
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
# assert sigfig.round(yield_str, 4) == sigfig.round(max_tensile_stress, 4)
# assert max_tensile_stress < yield_str
print("Maximum tensile stress = ", max_tensile_stress)
print("Max tensile stress exceeded by factor of ", max_tensile_stress/yield_str)

max_shear_stress = 2 * P / A
assert shear_str > max_shear_stress
# assert sigfig.round(shear_str, 4) == sigfig.round(max_shear_stress, 4)
print("Maximum shear stress = ", max_shear_stress)
print("Max shear stress exceeded by factor of ", max_shear_stress/shear_str)

print("Thickness = ", (R - r)*1000, " mm")

Vol = A * L
m_beam = Vol * density
print("Mass of the beam = ", m_beam, " kg")