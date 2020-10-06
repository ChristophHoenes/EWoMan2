import os
import numpy as np


def default_fitness(p, env):
    fit, e_p, e_e, t = env.play(pcont=np.asarray(p))
    return tuple([fit])


def multi_fitness(p, envs):
    fitnesses = []
    for env in envs:
        fit, e_p, e_e, t = env.play(pcont=np.asarray(p))
        fitnesses.append(fit)
    return tuple(fitnesses)

