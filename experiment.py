import sys, os
import numpy as np
import csv
import datetime
from statistics import mean
import pickle
from collections import defaultdict

from deap import creator, base

sys.path.insert(0, 'evoman')
from environment import Environment
from demo_controller import player_controller


def get_best_individuals(enemy=(1, 2, 5)):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("FitnessMulti", base.Fitness, weights=(1.0,) * len(enemy))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    top_individuals = defaultdict(list)

    seeds = [111, 222, 333, 444, 555, 666, 777, 888, 999, 1010]
    methods = ["scalarization", "nsga2_3"]
    for method in methods:
        if method == 'scalarization':
            prefix = 'scalarization'
            top5_type = 'top5'
        elif method == 'nsga2':
            prefix = 'nsga2'
            top5_type = 'top5'
        elif method == 'nsga2_2' or method == 'nsga2_3':
            prefix = 'nsga2'
            top5_type = 'my_top5'

        enemies_str = ("{}" + "_{}" * (len(enemy) - 1)).format(*enemy)

        for seed in seeds:

            top5_path = 'results/{}/{}_enemy{}_seed_{}/{}_iter_100'.format(method, prefix, enemies_str, seed, top5_type)
            top_ind = pickle.load(open(top5_path, "rb"))[0]
            top_individuals[method].append(top_ind)

    return top_individuals


if __name__ == "__main__":

    enemies = [1, 2, 3, 4, 5, 6, 7, 8]
    num_neurons = 10
    enemy_results = {}

    for en in enemies:

        experiment_name = 'experiment'
        if not os.path.exists(experiment_name):
            os.makedirs(experiment_name)

        env = Environment(experiment_name=experiment_name,
                          enemies=[en],
                          playermode="ai",
                          player_controller=player_controller(num_neurons),
                          enemymode="static",
                          level=2,
                          speed="fastest",
                          randomini="no",
                          contacthurt="player",
                          sound="off")

        top_individuals = get_best_individuals(enemy=(1, 2, 5))
        results = defaultdict(list)
        methods = ["scalarization", "nsga2_3"]
        for method in methods:
            for individual in top_individuals[method]:
                ind_results = []
                for iter in range(5):
                    fit, e_p, e_e, t = env.play(pcont=np.asarray(individual))
                    ind_results.append((e_p, e_e))
                mean_energies = tuple([mean(e) for e in zip(*ind_results)])
                results[method].append(mean_energies)

        enemy_results[en] = results

    pickle.dump(enemy_results, open("best_ind_results", "wb"))
