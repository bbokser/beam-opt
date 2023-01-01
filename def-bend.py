import numpy as np
import sigfig

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
I_max = P * L**3 / (3 * E * def_max)

print("Min Moment of Inertia for Max Deflection = ", I_max)

M_max = P * L
R_min = yield_str * I_max / M_max
r_min = (R_min**4 - I_max * 4 / np.pi)**0.25  # 4th root
A_max = np.pi * (R_min**2 - r_min**2)
assert R_min > r_min

print("R_min = ", R_min)
print("r_min = ", r_min)
print("A_max = ", A_max)

M_max = P * L
tensile_stress = M_max * R_min / I_max
assert sigfig.round(yield_str, 4) == sigfig.round(tensile_stress, 4)

max_shear_stress = 2 * P / A_max
assert shear_str > max_shear_stress
# print("Maximum shear stress = ", max_shear_stress)
print("Max shear stress exceeded by factor of ", max_shear_stress/shear_str)

# max_tensile_stress = M_max * R_min / I_max
# assert max_tensile_stress < yield_str
# print("Maximum tensile stress = ", max_tensile_stress)

print("Thickness = ", (R_min - r_min)*1000, " mm")

Vol = A_max * L
m_beam = Vol * density
print("Mass of the beam = ", m_beam, " kg")