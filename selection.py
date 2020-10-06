import numpy as np
from deap import tools
import random
from diversity import compute_centroids, diversity_gain


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


def deap_tournament_pairs(population, k=50, tournsize=3):
    parents = tools.selTournament(population, k=k, tournsize=tournsize)
    return zip(parents[::2], parents[1::2])


def deap_tournament(population, k=3, tournsize=2):
    return tools.selTournament(population, k=k, tournsize=tournsize)


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


def deap_roulette(population, k=50):
    return tools.selRoulette(population, k)


def deap_universal(population, k=50):
    return tools.selStochasticUniversalSampling(population, k)


def deap_best(population, k=3):
    return tools.selBest(population, k)

