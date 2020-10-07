import numpy as np


# moment of interia diversity
def diversity(population):
    pop = np.asarray(population)
    centroids = pop.mean(axis=0)
    return sum([np.square(ind-centroids).sum() for ind in pop])


def compute_centroids(population):
    pop = np.asarray(population)
    return pop.mean(axis=0)


def diversity_gain(centroids, individual):
    ind = np.asarray(individual)
    return np.square(ind - centroids).sum()


def crowding_distance_assignment(population):
    num_fitnesses = len(population[0].fitness.values)
    l = len(population)
    #distances = np.zeros(l)
    for f in range(num_fitnesses):
        sorted_pop = sorted(population, key=lambda p: p.fitness.values[f], reverse=True)
        sorted_pop[0].dist = sorted_pop[l-1].dist = np.inf
        for i in range(1, l-1):
            sorted_pop[i].dist += sorted_pop[i+1].fitness.values[f] - sorted_pop[i-1].fitness.values[f]
    return sorted_pop
