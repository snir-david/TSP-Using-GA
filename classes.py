import random

from main import CITIES
import numpy as np


class Individual:
    def __init__(self):
        pass


class Population:
    def __init__(self, size):
        self.populationSize = size
        self.population = []
        for i in range(size):
            c = Chromosome()
            c.random_init()
            self.population.append(c)


class Chromosome:
    def __init__(self):
        self.route = []

    def random_init(self):
        self.route = random.sample(CITIES, len(CITIES))

    def set_route(self, route_list):
        self.route = route_list


class Individual:
    def __init__(self):
        pass
