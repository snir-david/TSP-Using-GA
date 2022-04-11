import random
import numpy as np
import classes

POPULATION_SIZE = 10
CITIES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def crossover(c1, c2):
    offspring1 = [None] * len(CITIES)
    offspring2 = [None] * len(CITIES)
    offspring1_idx = 0
    offspring2_idx = 0
    idx1 = random.randint(0, len(CITIES) - 1)
    idx2 = random.randint(idx1, len(CITIES))
    diff = idx2 - idx1
    for i in range(idx1, idx2):
        offspring1[i] = c1.route[i]
        offspring2[i] = c2.route[i]
    for j in range(len(CITIES)):
        if c2.route[j] not in offspring1 and ((offspring1_idx + diff) < len(CITIES)):
            if offspring1_idx < idx1:
                offspring1[offspring1_idx] = c2.route[j]
            else:
                offspring1[offspring1_idx + diff] = c2.route[j]
            offspring1_idx += 1
        if c1.route[j] not in offspring2 and ((offspring2_idx + diff) < len(CITIES)):
            if offspring2_idx < idx1:
                offspring2[offspring2_idx] = c1.route[j]
            else:
                offspring2[offspring2_idx + diff] = c1.route[j]
            offspring2_idx += 1
    o1 = classes.Chromosome()
    o1.set_route(offspring1)
    o2 = classes.Chromosome()
    o2.set_route(offspring2)
    return o1, o2


def mutation(chromosome):
    print(chromosome.route)
    idx1 = random.randint(0, len(CITIES) - 1)
    idx2 = random.randint(0, len(CITIES) - 1)
    chromosome.route[idx1], chromosome.route[idx2] = chromosome.route[idx2], chromosome.route[idx1]
    chromosome.calc_fittness()
    print(chromosome.route)


def selection(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def fittness(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def init_population(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    p = classes.Population(10)
    for i in p.population:
        print(i.route)
    off1, off2 = crossover(p.population[0], p.population[1])
    mutation(off1)
