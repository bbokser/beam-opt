import numpy as np

m = 20  # kg
SF = 2  # safety factor
g = 9.81
shear_str_epoxy = 28e6
R = .01915  # m
len = 0.012  # m

P = m * g * SF

A_bond = 2* np.pi * R * len
shear_stress = P / A_bond 

assert shear_str_epoxy > shear_stress
print("Maximum shear stress = ", shear_stress, " Pa")
print("Shear Strength exceeded by factor of ", shear_stress/shear_str_epoxy)