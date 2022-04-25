import random
import numpy as np


def get_distance(chrom):
    return chrom.distance


class City:
    def __init__(self, x, y, id):
        self.id = id
        self.x = x
        self.y = y

    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)
        distance = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distance

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"


class Population:
    def __init__(self, size, cities):
        self.populationSize = size
        self.population = []
        self.weights = []
        self.init_population(cities)
        self.find_weights()

    def init_population(self, cities):
        for i in range(self.populationSize):
            c = Chromosome()
            c.random_init(cities)
            self.population.append(c)

    def find_weights(self):
        sum = 0
        for c in self.population:
            sum += c.fittness
        for c in self.population:
            self.weights.append((c.fittness / sum) * 100)

    def set_population(self, population_list):
        self.population.clear()
        self.population = [None] * len(population_list)
        for i in range(len(population_list)):
            self.population[i] = population_list[i]

    def get_fittest(self):
        fittest = self.population[0]
        for chrom in self.population:
            if chrom.fittness > fittest.fittness:
                fittest = chrom
        return fittest

    def get_average(self):
        sum = 0
        for chrom in self.population:
            sum += chrom.distance
        return sum / len(self.population)

    def get_worst_index(self):
        worst = self.population[0]
        idx = 0
        for i in range(len(self.population)):
            if self.population[i].fittness < worst.fittness:
                worst = self.population[i]
                idx = i
        return idx

    def sort_population_by_fitness(self):
        self.population.sort(key=get_distance)


class Chromosome:
    def __init__(self):
        self.route = []
        self.fittness = 0
        self.distance = 0

    def random_init(self, cities):
        self.route = random.sample(cities, len(cities))
        self.calc_fittness()

    def set_route(self, route_list):
        self.route = route_list
        self.calc_fittness()

    def calc_fittness(self):
        sum = 0
        for i in range(len(self.route) - 1):
            dist = self.route[i].distance(self.route[i + 1])
            sum += dist
        # print(self.route)
        sum += self.route[0].distance(self.route[len(self.route) - 1])
        self.distance = int(sum)
        self.fittness = float(1 / sum)

    def swap(self, i, j):
        self.route[i], self.route[j] = self.route[j], self.route[i]
        self.calc_fittness()
