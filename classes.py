import random
from main import CITIES


class Population:
    def __init__(self, size):
        self.populationSize = size
        self.population = []
        self.weights = []
        self.init_population()
        self.find_weights()

    def init_population(self):
        for i in range(self.populationSize):
            c = Chromosome()
            c.random_init()
            self.population.append(c)

    def find_weights(self):
        sum = 0
        for c in self.population:
            sum += c.fittness
        for c in self.population:
            self.weights.append((c.fittness / sum) * 100)

    def set_population(self, population_list):
        for i in range(len(population_list)):
            self.population[i] = population_list[i]

    def get_fittest(self):
        fittest = self.population[0]
        for chrom in self.population:
            if chrom.fittness > fittest.fittness:
                fittest = chrom
        return fittest

    def get_worst_index(self):
        worst = self.population[0]
        idx = 0
        for i in range(len(self.population)):
            if self.population[i].fittness < worst.fittness:
                worst = self.population[i]
                idx = i
        return idx


class Chromosome:
    def __init__(self):
        self.route = []
        self.fittness = 0
        self.distance = 0

    def random_init(self):
        self.route = random.sample(CITIES, len(CITIES))
        self.calc_fittness()

    def set_route(self, route_list):
        self.route = route_list
        self.calc_fittness()

    def calc_fittness(self):
        sum = 0
        for i in range(len(self.route) - 1):
            diff = abs(self.route[i + 1] - self.route[i])
            sum += diff
        sum += abs(self.route[0] - self.route[len(self.route)-1])
        self.distance = sum
        self.fittness = 1/sum

    def swap(self, i, j):
        self.route[i], self.route[j] = self.route[j], self.route[i]
        self.calc_fittness()
