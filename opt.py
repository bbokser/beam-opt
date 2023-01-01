import cvxpy as cp
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

R = cp.Variable()
# r = cp.Variable()
# R = cp.Variable(pos=True, name="R")
# r = cp.Variable(pos=True, name="r")

cost = R**2 - (R-0.001)**2
print("This objective function is", cost.curvature)

constr = []
constr += [R <= .15,
           R >= 0.05]
        #    R - r >= 0.001,
        #    4 * M * R / (np.pi * (R**4 - r**4)) <= yield_str,
        #    2 * P / (np.pi * (R**2 - r**2)) <= shear_str]

problem = cp.Problem(cp.Minimize(cost), constr)
# problem.solve(solver=cp.OSQP)  #, verbose=True)
problem.solve()
# problem.solve(qcp=True, verbose=True)

print(R.value)
print(r.value)
# if self.u.value is None or self.x.value is None:
#     raise Exception("\n *** QP FAILED *** \n")
