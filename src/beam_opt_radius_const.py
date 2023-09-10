import nlopt
import numpy as np


def opt_r(material, def_max, thickness_min, P, Lx, Ly, R, r0):
    E = material["E_flex"]
    shear_str = material["shear_str"]
    yield_str = material["flex_str"]
    My = P * Lx
    Mx = P * Ly

    def objfunc(x, grad):
        if grad.size > 0:
            grad[0] = - 2 * x[0]
        return R**2 - x[0]**2

    def shear_constr(x, grad):
        if grad.size > 0:
            grad[0] = np.pi * (-2 * Mx * x[0] * x[0] + \
                - 4 * x[0]**3 * P + \
                - shear_str * np.pi * (- x[0] * x[0]**4 + 3 * x[0]**5 - 2 * x[0]**3 * x[0]**2))
    
        return np.pi * (Mx * R * (R**2 - x[0]**2) + \
                        P * (R**4 - x[0]**4) - \
                        0.5 * shear_str * np.pi * (R**4 - x[0]**4) * (R**2 - x[0]**2))

    def tensile_constr(x, grad):
        if grad.size > 0:
            grad[0] = yield_str * np.pi * 4 * x[0]**3
        return 4 * My * R - yield_str * np.pi * (R**4 - x[0]**4)

    def def_constr(x, grad):
        if grad.size > 0:
            grad[0] = def_max * 12 * E * np.pi * x[0]**3
        return 4 * P * Lx**3 - def_max * 3 * E * np.pi * (R**4 - x[0]**4)

    opt = nlopt.opt(nlopt.LD_MMA, 1)
    opt.set_lower_bounds([0.01])
    opt.set_upper_bounds([R - thickness_min])
    opt.set_min_objective(objfunc)
    opt.add_inequality_constraint(lambda x, grad:shear_constr(x, grad), 1e-8)
    opt.add_inequality_constraint(lambda x, grad:tensile_constr(x, grad), 1e-8)
    # opt.add_inequality_constraint(lambda x, grad:thickness_constr(x, grad), 1e-8)
    opt.add_inequality_constraint(lambda x, grad:def_constr(x, grad), 1e-8)
    opt.set_xtol_rel(1e-6)
    
    x = opt.optimize([r0])
    minf = opt.last_optimum_value()
    print("optimum at ", R)
    print("minimum value = ", minf)
    print("result code = ", opt.last_optimize_result())
    print("\n")

    r = x[0]

    return r


