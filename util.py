from fitness import *
from mating import *
from mutation import *
from selection import *


def process_config(config, toolbox):
    toolbox.register("evaluate_fitness", select_fitness(config["fitness"]))
    toolbox.register("select_mating_partners", select_selection(config["mate_select"]))
    toolbox.register("mate", select_mating(config["mate"]))
    toolbox.register("mutate_offspring", select_mutation(config["mutate_offspring"]))
    toolbox.register("mutate_parents", select_mutation(config["mutate_parents"]))
    toolbox.register("select_survivors", select_selection(config["survive_select"]))


def select_fitness(fct_name):
    if fct_name == 'default':
        return default_fitness
    else:
        raise RuntimeError("Unknown type of fitness function encountered! Please check your config.")


def select_mating(fct_name):
    if fct_name == 'dummy':
        return average_parents
    elif fct_name == 'deap_xover_blend':
        return deap_xover_blend
    elif fct_name == 'deap_xover_onepoint':
        return deap_xover_onepoint
    elif fct_name == 'deap_xover_uniform':
        return deap_xover_uniform
    else:
        raise RuntimeError("Unknown type of mating function encountered! Please check your config.")


def select_mutation(fct_name):
    if fct_name == 'dummy':
        return gaussian_dummy_mutate
    elif fct_name == 'deap_mutate_shuffle':
        return deap_shuffle_mutation
    elif fct_name == 'deap_mutate_gaussian':
        return deap_gaussian_mutation
    elif fct_name == 'deap_mutate_polynomial':
        return deap_polynomialbounded_mutation
    else:
        raise RuntimeError("Unknown type of mutation function encountered! Please check your config.")


def select_selection(fct_name):
    if fct_name == 'dummy':
        return dummy_survivors
    elif fct_name == 'dummy_pairs':
        return select_k_strongest_pairs
    elif fct_name == 'deap_best':
        return deap_best
    elif fct_name == 'deap_tournament':
        return deap_tournament
    elif fct_name == 'deap_tournament_pairs':
        return deap_tournament_pairs
    elif fct_name == 'round_robin_tournament':
        return round_robin_tournament
    elif fct_name == 'diversity_round_robin':
        return diversity_round_robin_tournament
    elif fct_name == 'deap_roulette':
        return deap_roulette
    elif fct_name == 'deap_universal':
        return deap_universal
    else:
        raise RuntimeError("Unknown type of selection encountered! Please check your config.")
