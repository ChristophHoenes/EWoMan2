import sys, os
import numpy as np
import csv
import datetime
from statistics import mean
import pickle
from operator import itemgetter
from collections import defaultdict

from deap import creator, base

sys.path.insert(0, 'evoman')
from environment import Environment
from demo_controller import player_controller


if __name__ == "__main__":

    enemies = range(1, 9)

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("FitnessMulti", base.Fitness, weights=(1.0,) * len(enemies))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    with open("results/best_ind_results_enemy1_2_5", "rb") as f:
        data1 = pickle.load(f)
    with open("results/best_ind_results_enemy2_6_7", "rb") as f:
        data2 = pickle.load(f)

    data_list = [data1, data2]

    wins = defaultdict(int)
    gains = defaultdict(int)
    stats = defaultdict(list)

    for enemy in enemies:
        for d, data in enumerate(data_list):
            for method in data[enemy]:
                for ind, individual in enumerate(data[enemy][method]):
                    if individual[0] > individual[1]:
                        wins["{}_{}_{}".format(method, d, ind+1)] += 1
                    gains["{}_{}_{}".format(method, d, ind+1)] += individual[0] - individual[1]
                    stats["{}_{}_{}".format(method, d, ind+1)].append(individual)

    max_wins = max(wins.values())
    best_individual_num_wins_ids = [ind for ind in wins.keys() if wins[ind] == max_wins]
    best_individual_gain_id = max([(gains[key], key) for key in gains.keys()])[1]

    if best_individual_gain_id in best_individual_num_wins_ids:
        best_individual_num_wins_id = best_individual_gain_id
    else:
        best_individual_num_wins_id = max([(gains[key], key) for key in best_individual_num_wins_ids])[1]

    print("Best gain:", best_individual_gain_id)
    for enemy in enemies:
        print("Enemy {}: player energy: {}, ememy energy: {}".format(enemy, *stats[best_individual_gain_id][enemy-1]))
    print("Best number of wins:", best_individual_num_wins_id)
    for enemy in enemies:
        print("Enemy {}: player energy: {}, ememy energy: {}".format(enemy, *stats[best_individual_num_wins_id][enemy-1]))

    best_gain_info = best_individual_gain_id.split("_")
    trial_number = "_3" if best_gain_info[0] == "nsga2" else ""
    enemy_group = "1_2_5" if int(best_gain_info[1]) == 0 else "2_6_7"
    seed_number = int(best_gain_info[2]) * 111 if int(best_gain_info[2]) <= 9 else 1010
    top = "my_" if best_gain_info[0] == "nsga2" else ""
    best_gain_path = "results/{}{}/{}_enemy{}_seed_{}/{}top5_iter_100".format(best_gain_info[0], trial_number, best_gain_info[0], enemy_group, seed_number, top)
    with open(best_gain_path, "rb") as f:
        best_gain = pickle.load(f)
    print(best_gain[0])

    best_win_info = best_individual_num_wins_id.split("_")
    trial_number = "_3" if best_win_info[0] == "nsga2" else ""
    enemy_group = "1_2_5" if int(best_win_info[1]) == 0 else "2_6_7"
    seed_number = int(best_win_info[2]) * 111 if int(best_win_info[2]) <= 9 else 1010
    top = "my_" if best_win_info[0] == "nsga2" else ""
    best_win_path = "results/{}{}/{}_enemy{}_seed_{}/{}top5_iter_100".format(best_win_info[0], trial_number, best_win_info[0],
                                                              enemy_group, seed_number, top)
    with open(best_win_path, "rb") as f:
        best_win = pickle.load(f)
    print(best_win[0])

    np.savetxt("70.txt", np.asarray(best_gain[0]))
