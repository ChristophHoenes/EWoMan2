import os
import numpy as np


def default_fitness(p, env):
    fit, e_p, e_e, t = env.play(pcont=np.asarray(p))
    return fit

