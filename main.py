import random

from classes import *

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
    o1 = Chromosome()
    o1.set_route(offspring1)
    o2 = Chromosome()
    o2.set_route(offspring2)
    return o1, o2


def mutation(chromosome):
    rand = random.randint(0, 100)
    if rand < 25:
        idx1 = random.randint(0, len(CITIES) - 1)
        idx2 = random.randint(0, len(CITIES) - 1)
        chromosome.route[idx1], chromosome.route[idx2] = chromosome.route[idx2], chromosome.route[idx1]
        chromosome.calc_fittness()


def selection(population):
    parents = random.choices(population=population.population, cum_weights=population.weights, k=2)
    return parents


if __name__ == '__main__':
    # initialize population
    generation_count = 0
    population = Population(POPULATION_SIZE)
    print(sum(population.weights))
    for i in range(1000000):
        new_population = []
        parents = selection(population)
        half = int(POPULATION_SIZE / 2)
        for j in range(half):
            off1, off2 = crossover(parents[0], parents[1])
            new_population.append(off2)
            new_population.append(off1)
        for offspring in new_population:
            mutation(offspring)
        population.set_population(new_population)
        print(f"Generation count: {generation_count} fittest: {population.get_fittest().fittness} ")
        generation_count += 1
    print(f"Generation count: {generation_count} fittest: {population.get_fittest().fittness} ")
