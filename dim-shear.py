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

R = 0.1  # user-chosen upper limit
r = np.sqrt(R**2 - P/(shear_str * np.pi/2))  # solve for r given R and shear strength
I = np.pi * (R**4 - r**4)/4
print("Moment of Inertia = ", I)

A = np.pi * (R**2 - r**2)
assert R > r
print("R = ", R)
print("r = ", r)
print("Cross-Sectional Area = ", A)
# print("A_check = ", A_check)

M_max = P * L
max_tensile_stress = M_max * R / I
# assert sigfig.round(yield_str, 4) == sigfig.round(max_tensile_stress, 4)
# assert max_tensile_stress < yield_str
print("Max tensile stress exceeded by factor of ", max_tensile_stress/yield_str)
# print("Maximum tensile stress = ", max_tensile_stress)

max_shear_stress = 2 * P / A
# assert shear_str > max_shear_stress
assert sigfig.round(shear_str, 4) == sigfig.round(max_shear_stress, 4)
print("Maximum shear stress = ", max_shear_stress)

print("Thickness = ", (R - r)*1000, " mm")

Vol = A * L
m_beam = Vol * density
print("Mass of the beam = ", m_beam, " kg")