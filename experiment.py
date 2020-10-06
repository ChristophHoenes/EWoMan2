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


def get_best_individuals(enemy=2):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    top_individuals = defaultdict(list)

    seeds = [111, 222, 333, 444, 555, 666, 777, 888, 999, 1010]
    methods = ["method_1", "method2", "method3"]
    for method in methods:
        if method == 'method_1':
            prefix = 'roundrobin'
        elif method == 'method2':
            prefix = 'diversity_roundrobin'
        elif method == "method3":
            prefix = "diversity_075_roundrobin"
        for seed in seeds:

            top5_path = 'results/{}/{}_enemy{}_seed_{}/top5_iter_30'.format(method, prefix, enemy, seed)
            top_ind = pickle.load(open(top5_path, "rb"))[0]
            top_individuals[method].append(top_ind)

    return top_individuals


if __name__ == "__main__":

    enemies = [2,6,7]
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

        top_individuals = get_best_individuals(enemy=en)
        results = defaultdict(list)
        methods = ["method_1", "method3"]
        for method in methods:
            for individual in top_individuals[method]:
                ind_results = []
                for iter in range(5):
                    os.chdir('./evoman_framework')
                    fit, e_p, e_e, t = env.play(pcont=np.asarray(individual))
                    os.chdir('../')
                    ind_results.append(e_p-e_e)
                results[method].append(mean(ind_results))

        enemy_results[en] = results

    pickle.dump(enemy_results, open("best_ind_results", "wb"))
