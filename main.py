import random

from classes import *

POPULATION_SIZE = 10000
MUTATION_RATE = 10
NUMBER_OF_GENERATIONS = 1000
CITIES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def crossover(parent1, parent2): \
        # init
    offspring1 = [None] * len(CITIES)
    offspring2 = [None] * len(CITIES)
    offspring1_idx = 0
    offspring2_idx = 0
    # random
    idx1 = random.randint(0, len(CITIES) - 1)
    idx2 = random.randint(idx1, len(CITIES))
    diff = idx2 - idx1
    # taking from idx1 to idx2 the part of the appropriate parent
    for i in range(idx1, idx2):
        offspring1[i] = parent1.route[i]
        offspring2[i] = parent2.route[i]
    # rest of crossover
    for j in range(len(CITIES)):
        if parent2.route[j] not in offspring1 and ((offspring1_idx + diff) < len(CITIES)):
            if offspring1_idx < idx1:
                offspring1[offspring1_idx] = parent2.route[j]
            else:
                offspring1[offspring1_idx + diff] = parent2.route[j]
            offspring1_idx += 1
        if parent1.route[j] not in offspring2 and ((offspring2_idx + diff) < len(CITIES)):
            if offspring2_idx < idx1:
                offspring2[offspring2_idx] = parent1.route[j]
            else:
                offspring2[offspring2_idx + diff] = parent1.route[j]
            offspring2_idx += 1
    # return Chromosomes
    o1, o2 = Chromosome(), Chromosome()
    o1.set_route(offspring1), o2.set_route(offspring2)
    return o1, o2


def mutation(chromosome, mutation_rate):
    for idx in range(len(chromosome.route)):
        if random.randint(0, 100) < mutation_rate:
            idx2 = random.randint(0, len(CITIES) - 1)
            chromosome.swap(idx, idx2)


def selection(population):
    parents = []
    parents.append((random.choices(population=population.population, cum_weights=population.weights, k=1))[0])
    tmp = random.choices(population=population.population, cum_weights=population.weights, k=1)
    while parents[0] == tmp[0]:
        tmp = random.choices(population=population.population, cum_weights=population.weights, k=1)
    parents.append(tmp[0])
    print(f"parents: {parents[0].route}, {parents[1].route}")
    return parents


def elite(old_population, new_population):
    old_fittest = old_population.get_fittest()
    new_fittest = new_population.get_fittest()
    if old_fittest.fittness > new_fittest.fittness:
        worst_idx = new_population.get_worst_index()
        new_population.population[worst_idx] = old_fittest


def new_gen(current_gen, mutation_rate):
    next_gen = Population(POPULATION_SIZE)
    new_population = []
    parents = selection(current_gen)
    for j in range(int(POPULATION_SIZE / 2)):
        off1, off2 = crossover(parents[0], parents[1])
        new_population.append(off2)
        new_population.append(off1)
    for offspring in new_population:
        mutation(offspring, mutation_rate)
    next_gen.set_population(new_population)
    elite(old_population=current_gen, new_population=next_gen)
    return next_gen


if __name__ == '__main__':
    # initialize population
    generation_count = 0
    population = Population(POPULATION_SIZE)
    print(sum(population.weights))
    for i in range(NUMBER_OF_GENERATIONS):
        population = new_gen(population, MUTATION_RATE)
        idx = population.get_worst_index()
        print(f"Generation count: {generation_count} fittest: {population.get_fittest().distance} route - {population.get_fittest().route}\n"
              f"the worst distance is: {population.population[idx].distance}")
        generation_count += 1
    print(f"Generation count: {generation_count} fittest: {population.get_fittest().fittness} ")
