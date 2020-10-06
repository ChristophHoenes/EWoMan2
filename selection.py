from functools import cmp_to_key
import random

import numpy as np
from deap import tools

from diversity import compute_centroids, diversity_gain, crowding_distance_assignment
from nsga2 import fast_non_dominated_sort, crowding_operator_cmp


#def select_strongest_pairs(fitness, num_matings=5):
#    sorted_fit = np.argsort(fitness)
#    pairs = sorted_fit[:2*num_matings].reshape([num_matings, 2])
#    return list(map(tuple, pairs))

def select_k_strongest_pairs(population, k=9):
    fitness = [p.fitness.values[0] for p in population]
    sorted_idxs = [x for x, y in sorted(enumerate(fitness), key=lambda tup: tup[1])]
    top_k = sorted_idxs[:k]
    parents = [population[top_k[np.random.choice(len(top_k))]] for i in range(2*len(population))]
    return zip(parents[::2], parents[1::2])


def dummy_survivors(population, k=3):
    fitness = [p.fitness.values[0] for p in population]
    sorted_idxs = [x for x, y in sorted(enumerate(fitness), key=lambda tup: tup[1])]
    top_k = sorted_idxs[:k]
    return [population[i] for i in top_k]


def deap_tournament_pairs(population, k=50, tournsize=3, fit_attr="fitness"):
    parents = tools.selTournament(population, k=k, tournsize=tournsize, fit_attr=fit_attr)
    return zip(parents[::2], parents[1::2])


def deap_tournament(population, k=3, tournsize=2, fit_attr="fitness"):
    return tools.selTournament(population, k=k, tournsize=tournsize, fit_attr=fit_attr)


def round_robin_tournament(population, k=100, tournsize=10):
    wins = np.zeros(len(population))
    for id, x in enumerate(population):
        for j in range(tournsize):
            rival = np.random.choice(len(population))
            if x.fitness.values[0] > population[rival].fitness.values[0]:
                wins[id] += 1
    winner_idx = wins.argsort()[::-1][:k]
    survivors = [population[i] for i in winner_idx]
    return survivors


def diversity_round_robin_tournament(population, k=100, tournsize=10, alpha=0.5):
    centroids = compute_centroids(population)
    diversity_gains = list(map(lambda p: diversity_gain(centroids, p), population))
    min_div = min(diversity_gains)
    diversity_range = max(diversity_gains) - min_div
    diversity_normalized = [(d - min_div) / diversity_range for d in diversity_gains]

    fitness = [ind.fitness.values[0] for ind in population]
    min_fit = min(fitness)
    fitness_range = max(fitness) - min_fit
    fitness_normalized = [(f - min_fit) / fitness_range for f in fitness]

    wins = np.zeros(len(population))
    for id, x in enumerate(population):
        score = (1 - alpha) * fitness_normalized[id] + alpha * diversity_normalized[id]
        for j in range(tournsize):
            rival = np.random.choice(len(population))
            rival_score = (1 - alpha) * fitness_normalized[rival] + alpha * diversity_normalized[rival]
            if score > rival_score:
                wins[id] += 1
    winner_idx = wins.argsort()[::-1][:k]
    survivors = [population[i] for i in winner_idx]
    return survivors


def deap_roulette(population, k=50, fit_attr="fitness"):
    return tools.selRoulette(population, k, fit_attr=fit_attr)


def deap_universal(population, k=50, fit_attr="fitness"):
    return tools.selStochasticUniversalSampling(population, k, fit_attr=fit_attr)


def deap_best(population, k=3, fit_attr="fitness"):
    return tools.selBest(population, k, fit_attr=fit_attr)


def frontier_level_selection_with_crowding_distance_tiebreak(population, k=100):
    new_population = []
    population, frontiers = fast_non_dominated_sort(population)
    i = 1
    while len(new_population) + len(frontiers[i]) <= k:
        f = [population[ind_id] for ind_id in frontiers[i]]
        crowding_distance_assignment(f)
        new_population += f
        i += 1
    # last front that doesn't fit completely in the new population
    f = [population[ind_id] for ind_id in frontiers[i]]
    # fill the remaining spots in new population based on crowding operator
    sorted(f, key=cmp_to_key(crowding_operator_cmp))
    new_population += f[:k-len(new_population)]
    return new_population


def deterministic_crowding(partners, offspring, relations, k):
    winners = []
    for idx in relations:
        children = (offspring[relations[idx][0]], offspring[relations[idx][1]])
        parents = partners[idx]
        if dist(children[0], parents[0]) + dist(children[1], parents[1]) < dist(children[0], parents[1]) + dist(children[1], parents[0]):
            tournaments = [(children[0], parents[0]), (children[1], parents[1])]
        else:
            tournaments = [(children[0], parents[1]), (children[1], parents[0])]
        for tourn in tournaments:
            if tourn[0] > tourn[1]:
                winners.append(tourn[0])
            else:
                winners.append(tourn[1])
    assert len(winners) == k
    return winners

def dist(ind1, ind2):
    return np.abs(np.array(ind1)-np.array(ind2)).sum()

