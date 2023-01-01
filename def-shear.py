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

A_max = 2 * P / shear_str
r_min = np.sqrt((4 * I_max - (A_max**2)/np.pi)/(2 * A_max))
R_min = np.sqrt(A_max / np.pi + r_min**2)
A_check = np.pi * (R_min**2 - r_min**2)
assert R_min > r_min
assert sigfig.round(A_max, 4) == sigfig.round(A_check, 4)

print("R_min = ", R_min)
print("r_min = ", r_min)
print("A_max = ", A_max)
# print("A_check = ", A_check)

M_max = P * L
tensile_stress = M_max * R_min / I_max
assert tensile_stress < yield_str
print("Maximum tensile stress = ", tensile_stress)

print("Thickness = ", (R_min - r_min)*1000, " mm")

Vol = A_max * L
m_beam = Vol * density
print("Mass of the beam = ", m_beam, " kg")