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
