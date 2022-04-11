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
        self.fittness = 0

    def random_init(self):
        self.route = random.sample(CITIES, len(CITIES))
        self.calc_fittness()

    def set_route(self, route_list):
        self.route = route_list
        self.calc_fittness()

    def calc_fittness(self):
        sum = 0
        for i in range(len(self.route) - 2):
            diff = abs(self.route[i + 1] - self.route[i])
            sum += diff
        self.fittness = sum


class Individual:
    def __init__(self):
        pass
