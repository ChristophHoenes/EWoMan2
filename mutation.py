import numpy as np
from deap import tools


def gaussian_dummy_mutate(population, mutate_prob=0.1):
    num_mutate = round(len(population) * mutate_prob)
    for m in range(num_mutate):
        mutate_individual = population[np.random.choice(len(population))]
        for gene in range(round(len(mutate_individual) * mutate_prob)):
            mutate_gene = np.random.choice(len(mutate_individual))
            mutate_individual[mutate_gene] += np.random.normal(loc=0, scale=0.5)
    return population


def non_uniform_mutate(population, mutation_step_size=0.05):
    for individual in population:
        for gene in individual:
            gene += np.random.normal(0, mutation_step_size)
    
    return population


def deap_shuffle_mutation(population, ind_prob=0.2, mprob=0.1):
    mutant_selection = np.random.choice(2, size=len(population), p=[1-ind_prob, ind_prob])
    return [tools.mutShuffleIndexes(ind, mprob)[0] if mutant_selection[i] else ind for i, ind in enumerate(population)]


def deap_gaussian_mutation(population, mean=0, std=1, ind_prob=0.2, mprob=0.1):
    mutant_selection = np.random.choice(2, size=len(population), p=[1-ind_prob, ind_prob])
    return [tools.mutGaussian(ind, mean, std, mprob)[0]
            if mutant_selection[i] else ind for i, ind in enumerate(population)]


def deap_polynomialbounded_mutation(population, similarity=0.5, low=1, up=-1, ind_prob=0.2, mprob=0.1):
    mutant_selection = np.random.choice(2, size=len(population), p=[1-ind_prob, ind_prob])
    return [tools.mutPolynomialBounded(ind, similarity, low, up, mprob)[0]
            if mutant_selection[i] else ind for i, ind in enumerate(population)]
