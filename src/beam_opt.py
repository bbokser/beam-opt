import nlopt
import numpy as np


def opt(material, def_max, thickness_min, P, Lx, Ly):
    E = material["E"]
    shear_str = material["shear_str"]
    yield_str = material["yield_str"]
    My = P * Lx
    Mx = P * Ly

    def objfunc(x, grad):
        if grad.size > 0:
            grad[0] = 2 * x[0]  # partial derivatives
            grad[1] = - 2 * x[1]
        return x[0]**2 - x[1]**2

    def shear_constr(x, grad):
        if grad.size > 0:
            grad[0] = np.pi * (3 * Mx * x[0]**2 + \
                - Mx * x[1]**2 + \
                4 * x[0]**3 * P + \
                - shear_str * np.pi  * (3 * x[0]**5 - 2 * x[0]**3 * x[1]**2 - x[0] * x[1]**4))
            grad[1] = np.pi * (-2 * Mx * x[0] * x[1] + \
                - 4 * x[1]**3 * P + \
                - shear_str * np.pi * (- x[1] * x[0]**4 + 3 * x[1]**5 - 2 * x[1]**3 * x[0]**2))
    
        return np.pi * (Mx * x[0] * (x[0]**2 - x[1]**2) + \
                        P * (x[0]**4 - x[1]**4) - \
                        0.5 * shear_str * np.pi * (x[0]**4 - x[1]**4) * (x[0]**2 - x[1]**2))

    def tensile_constr(x, grad):
        if grad.size > 0:
            grad[0] = 4 * My - yield_str * np.pi * 4 * x[0]**3
            grad[1] = yield_str * np.pi * 4 * x[1]**3
        return 4 * My * x[0] - yield_str * np.pi * (x[0]**4 - x[1]**4)

    def def_constr(x, grad):
        if grad.size > 0:
            grad[0] = -def_max * 12 * E * np.pi * x[0]**3 
            grad[1] = def_max * 12 * E * np.pi * x[1]**3
        return 4 * P * Lx**3 - def_max * 3 * E * np.pi * (x[0]**4 - x[1]**4)

    def thickness_constr(x, grad):
        if grad.size > 0:
            grad[0] = -1
            grad[1] = 1
        return -x[0] + x[1] + thickness_min

    opt = nlopt.opt(nlopt.LD_MMA, 2)
    min = 0.01
    max = 0.5
    opt.set_lower_bounds([min, min-thickness_min])
    opt.set_upper_bounds([max, max-thickness_min])
    opt.set_min_objective(objfunc)
    opt.add_inequality_constraint(lambda x, grad:shear_constr(x, grad), 1e-8)
    opt.add_inequality_constraint(lambda x, grad:tensile_constr(x, grad), 1e-8)
    opt.add_inequality_constraint(lambda x, grad:thickness_constr(x, grad), 1e-8)
    opt.add_inequality_constraint(lambda x, grad:def_constr(x, grad), 1e-8)
    opt.set_xtol_rel(1e-6)
    R0 = 0.04 # P * 0.0002  # heuristic for warm starting... :(
    R0 = np.clip(R0, min, max)
    print("Using R0 = ", R0)
    # x = opt.optimize([0.019, 0.018])
    # x = opt.optimize([0.029, 0.028])
    # x = opt.optimize([0.046, 0.045])
    x = opt.optimize([R0, R0 - thickness_min])
    minf = opt.last_optimum_value()
    print("optimum at ", x[0], ", ", x[1])
    print("minimum value = ", minf)
    print("result code = ", opt.last_optimize_result())
    print("\n")

    R = x[0]
    r = x[1]

    return R, r


