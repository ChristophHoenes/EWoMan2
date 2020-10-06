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
    num_fitnesses = len(population[0].fitness)
    l = len(population)
    distances = np.zeros(l)
    for f in range(num_fitnesses):
        fitnesses = sorted(population, key=population.fitness[f], reverse=True)
        distances[0] = distances[l-1] = np.inf
        for i in range(1, l-1):
            distances[i] += population[i+1].fitness[f] - population[i-1].fitness[f]

