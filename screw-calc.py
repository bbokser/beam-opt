import numpy as np

m = 20  # kg
SF = 2  # safety factor
g = 9.81
len = 0.012  # m

tensile_str_screw = 1.17e9
r_screw = 0.0025 * 0.5

P = m * g * SF

A_screw = np.pi * r_screw ** 2
tensile_stress = P / A_screw 

assert tensile_str_screw > tensile_stress
print("Maximum stress = ", tensile_stress, " Pa")
print("Yield Strength exceeded by factor of ", tensile_stress/tensile_str_screw)