import nlopt
import numpy as np


def opt(material, L, def_max, P, M, M_axial):
    E = material["E"]
    shear_str = material["shear_str"]
    yield_str = material["yield_str"]
    min_thickness = material["min_thickness"]

    def objfunc(x, grad):
        if grad.size > 0:
            grad[0] = 2 * x[0]  # partial derivatives
            grad[1] = - 2 * x[1]
        return x[0]**2 - x[1]**2

    def shear_constr(x, grad):
        if grad.size > 0:
            grad[0] = np.pi * M_axial * x[0] * (2 * x[0]**2 + (x[0]**2 - x[1]**2)) + \
                4 * x[0]**3 * P * np.pi + \
                - np.pi**2 * shear_str * (2 * x[0]**3 * (x[0]**2 - x[1]**2) - x[0] * (x[0]**4 - x[1]**4))
            grad[1] = - 2 * M_axial * x[0] * x[1] * np.pi * 2 + \
                - 8 * x[1]**3 * P + \
                - np.pi**2 * x[1]**2 * shear_str * (2 * x[1] * (x[0]**2 - x[1]**2) + (x[0]**4 - x[1]**4))
        return M_axial * x[0] * np.pi * (x[0]**2 - x[1]**2)  + P * np.pi * (x[0]**4 - x[1]**4) - shear_str * np.pi**2 * (x[0]**4 - x[1]**4) * (x[0]**2 - x[1]**2)

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

    R = x[0]
    r = x[1]

    return R, r


