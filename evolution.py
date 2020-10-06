# standard library imports
import argparse
import json
import pickle
import sys
import os
from time import time, strftime, gmtime

# third party imports
import numpy as np
from deap import creator, base, tools, algorithms
from scoop import futures

# local imports
sys.path.insert(0, 'evoman')
from environment import Environment
from util import process_config
from representations import select_representation
from diversity import diversity, diversity_gain


def start_evolution(args, config):

    # define deap individuals to maximize fitness value
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # setup deap toolbox and statistics
    toolbox = base.Toolbox()
    top5 = tools.HallOfFame(5)
    stats = tools.Statistics(lambda x: x.fitness.values)
    stats.register("mean", np.mean)
    stats.register("std", np.std)
    stats.register("max", np.max)
    stats.register("min", np.min)
    stats.register("diversity", diversity)
    logs = [tools.Logbook()]
    logs[-1].header = "generation", "fit_evaluations", "mean", "std", "max", "min", "diversity"
    fit_evaluations = 0

    # check multiprocessing
    if args.multiprocessing:
        toolbox.register("map", futures.map)
    else:
        toolbox.register("map", map)

    # create directory for experiment results
    save_dir = "{}_enemy{}_seed_{}".format(args.config.split(".json")[0], args.enemies[0], args.seed)
    save_path = os.path.join(os.getcwd(), save_dir)
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # register desired evolution components
    process_config(config, toolbox)

    # pick problem representation
    rep = select_representation(args, toolbox)
    # initialize controller that handles the representation
    controller = rep.get_controller()

    #create folder for experiment
    exp_name = "specialist_{}".format(args.enemies)
    if not os.path.exists(exp_name):
        os.mkdir(exp_name)

    # create environment
    env = Environment(experiment_name=exp_name,
                      enemies=args.enemies,
                      playermode="ai",
                      player_controller=controller,
                      enemymode="static",
                      level=args.level,
                      speed="fastest",
                      randomini=args.random_loc,
                      contacthurt=args.contacthurt,
                      sound="off")

    # create initial population
    if args.init_pop == 'random':
        population = rep.create_population(args.pop_size)
    else:
        population = pickle.load(open(args.init_pop, "rb"))
    # save initial population
    pickle.dump(population, open(os.path.join(save_path, "initial_population"), "wb"))

    # loop through training iterations
    # test fitness of population
    fitness = list(map(lambda p: toolbox.evaluate_fitness(p, env), population))
    fit_evaluations += len(population)

    # assign fitness to corresponding individuals
    for ind, fit in zip(population, fitness):
        ind.fitness.values = (fit,)

    # record statistics and save intermediate results
    top5.update(population)
    record = stats.compile(population)
    logs[-1].record(generation=0, fit_evaluations=fit_evaluations, **record)
    # print progress
    print(logs[-1].stream)

    for i in range(1, args.num_iter+1):

        # Evolution components

        # mating selection
        partners = toolbox.select_mating_partners(population, **config["mate_select_args"])

        # mating mechanism (creating offspring from selection) and random mutation
        # clone parents first
        parent_clones = [tuple(toolbox.clone(ind) for ind in tup) for tup in partners]
        offspring = toolbox.mate(parent_clones, **config["mate_args"])

        # mutation of parent generation (optional)
        # population = toolbox.mutate_parents(population, **config["mut_pop_args"])
        # random mutations of offspring
        offspring = toolbox.mutate_offspring(offspring, **config["mut_off_args"])

        # test fitness of offspring
        fitness = list(toolbox.map(lambda p: toolbox.evaluate_fitness(p, env), offspring))
        fit_evaluations += len(offspring)

        # assign fitness to corresponding individuals
        for ind, fit in zip(offspring, fitness):
            ind.fitness.values = (fit,)

        # next generation consists of the survivors of the previous and the offspring
        population = population + offspring
        # survivor selection (define population of next iteration; which individuals are kept)
        population = toolbox.select_survivors(population, **config["survive_args"])

        # record statistics and save intermediate results
        top5.update(population)
        record = stats.compile(population)
        logs[-1].record(generation=i, fit_evaluations=fit_evaluations, **record)
        # print progress
        print(logs[-1].stream, flush=True)
        # stop last iteration after evaluation of final population
        if i == args.num_iter:
            break

    # save results
    pickle.dump(population, open(os.path.join(save_path, "latest_population_iter_{}".format(i)), "wb"))
    pickle.dump(logs, open(os.path.join(save_path, "logs_iter_{}".format(i)), "wb"))
    pickle.dump(top5, open(os.path.join(save_path, "top5_iter_{}".format(i)), "wb"))
    pickle.dump(config, open(os.path.join(save_path, "config"), "wb"))
    pickle.dump(args, open(os.path.join(save_path, "args"), "wb"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evolution Parameters.')
    parser.add_argument('--num_iter', default=30, type=int,
                        help='Number of iterations of the evolution (number of generated generations).')
    parser.add_argument('--num_neurons',  default=10, type=int,
                        help='Number of neurons used for the population.')
    parser.add_argument('--enemies', default=[2], nargs='+', type=int,
                        help='ID(s) of the enemy to specialize.')
    parser.add_argument('--level', default=2, type=int,
                        help='Difficulty of the game.')
    parser.add_argument('--random_loc', default="no", type=str, choices=["yes", "no"],
                        help='Whether or not to randomly initialize location of enemy.')
    parser.add_argument('--contacthurt', default="player", type=str, choices=["player", "enemy"],
                        help='Who is hurt by contact with the opponent.')
    parser.add_argument('--pop_size', default=100, type=int,
                        help='Population size (initial number of individuals).')
    parser.add_argument('--config', default="deap_roundrobin.json", type=str,
                        help='Configuration file that specifies some parameters.')
    parser.add_argument('--seed', default=None, type=int,
                        help='Seed for numpy random functions.')
    parser.add_argument('--init_pop', default='random', type=str,
                        help='Path to initial population file (default: random initialization).')
    parser.add_argument('--multiprocessing', default=False, type=bool,
                        help='Whether or not to use multiprocessing.')
    parser.add_argument('--server', default=False, type=bool,
                        help='Whether or not program is run on a UNIX server.')
    parser.add_argument('--representation', default="Neurons", type=str, choices=["Neurons"],
                        help='Type of problem representation.')

    args = parser.parse_args()

    # set dummy video device if run on linux server
    if args.server:
        os.environ["SDL_VIDEODRIVER"] = "dummy"

    # set seed
    if args.seed is not None:
        np.random.seed(args.seed)

    # load config from file
    with open('configs/{}'.format(args.config)) as c:
        config = json.loads(c.read())

    # print config
    for key in config.keys():
        print(key, ":", config[key])

    start_time = time()
    start_evolution(args, config)
    end_time = time()
    print("Finished {} generations with population size of {} in {} minutes".format(args.num_iter, args.pop_size,
                                                                                    (end_time-start_time)/60))
