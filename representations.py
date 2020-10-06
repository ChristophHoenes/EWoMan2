import json
import numpy as np
import os
import sys
from abc import ABC, abstractmethod

from deap import creator, base, tools, algorithms

from demo_controller import player_controller


NUM_SENSORS = 20
NUM_ACTIONS = 5


def select_representation(args, toolbox):
    if args.representation == "Neurons":
        return NeuronRep(args.num_neurons, toolbox=toolbox)
    else:
        raise RuntimeError('Unknown representation type encountered!')


class Representation(ABC):

    def __init__(self, config):
        with open('configs/{}'.format(config)) as c:
            self.config = json.loads(c)
        super(Representation, self).__init__()

    @abstractmethod
    def get_controller(self):
        raise NotImplementedError

    @abstractmethod
    def create_population(self):
        raise NotImplementedError


class NeuronRep(Representation):

    def __init__(self, num_neurons, toolbox=None):
        self.config = {"num_neurons": num_neurons,
                       "num_params": (NUM_SENSORS + 1) * num_neurons + (num_neurons + 1) * NUM_ACTIONS}
        toolbox.register("attr_float", np.random.uniform, -1, 1)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=self.config["num_params"])
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        self.toolbox = toolbox

    def get_controller(self):
        return player_controller(self.config['num_neurons'])

    def create_population(self, population_size):
        return self.toolbox.population(n=population_size)
