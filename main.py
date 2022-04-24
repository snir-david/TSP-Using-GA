import sys
from timeit import default_timer as timer
import matplotlib.pyplot as plt
from classes import *

POPULATION_SIZE = 1000
ELITE_SIZE = int(POPULATION_SIZE * 0.05)
MUTATION_RATE = 10
NUMBER_OF_GENERATIONS = 1000


# drawing plot according to the num of iteration and loss cost
def draw_plot(x, y):
    plt.plot(x, y)
    plt.xlabel("Generation")
    plt.ylabel("Distance")
    plt.show()


def init_cities(cities_list):
    cities = []
    for i in range(len(cities_list)):
        c = City(cities_list[i][0], cities_list[i][1], i)
        cities.append(c)
    return cities


def crossover(parent1, parent2):
    # init
    size = len(parent1.route)
    offspring1 = [None] * size
    offspring2 = [None] * size
    offspring1_idx = 0
    offspring2_idx = 0
    # random
    # idx1 = random.randint(1, size - 1)
    idx1 = random.randint(0, size - 1)
    idx2 = random.randint(idx1, size)
    diff = idx2 - idx1
    # taking from idx1 to idx2 the part of the appropriate parent
    for i in range(idx1, idx2):
        offspring1[i] = parent1.route[i]
        offspring2[i] = parent2.route[i]
    # rest of crossover
    for j in range(size):
        if parent2.route[j] not in offspring1 and ((offspring1_idx + diff) < size):
            if offspring1_idx < idx1:
                offspring1[offspring1_idx] = parent2.route[j]
            else:
                offspring1[offspring1_idx + diff] = parent2.route[j]
            offspring1_idx += 1
        if parent1.route[j] not in offspring2 and ((offspring2_idx + diff) < size):
            if offspring2_idx < idx1:
                offspring2[offspring2_idx] = parent1.route[j]
            else:
                offspring2[offspring2_idx + diff] = parent1.route[j]
            offspring2_idx += 1
    # return Chromosomes
    o1, o2 = Chromosome(), Chromosome()
    o1.set_route(offspring1), o2.set_route(offspring2)
    return o1, o2


def one_point_crossover(parent1, parent2):
    # init
    size = len(parent1.route)
    offspring1 = []
    offspring2 = []
    # random
    point = random.randint(1, size - 1)
    offspring1.extend(parent1.route[0:point])
    offspring2.extend(parent2.route[0:point])
    for i in range(size):
        if parent2.route[i] not in offspring1:
            offspring1.append(parent2.route[i])
        if parent1.route[i] not in offspring2:
            offspring2.append(parent1.route[i])
    # return Chromosomes
    o1, o2 = Chromosome(), Chromosome()
    o1.set_route(offspring1), o2.set_route(offspring2)
    return o1, o2


def mutation(chromosome, mutation_rate: int):
    for idx in range(1, len(chromosome.route)):
        if random.randint(0, 100) < mutation_rate:
            idx2 = random.randint(1, len(chromosome.route) - 1)
            chromosome.swap(idx, idx2)


def selection(population):
    return random.choices(population=population.population, cum_weights=population.weights, k=2)


def random_selection(population):
    return random.choices(population=population.population, k=2)


def elite(old_population, new_population, elite_size):
    size = len(new_population.population) - 1
    old_population.sort_population_by_fitness()
    new_population.sort_population_by_fitness()
    for i in range(elite_size):
        if old_population.population[i].fittness > new_population.population[size - i].fittness:
            new_population.population[size - i] = old_population.population[i]


def new_gen(current_gen, mutation_rate: int, cities):
    next_gen = Population(POPULATION_SIZE, cities)
    new_population = []
    for j in range(int(POPULATION_SIZE / 2)):
        parents = random_selection(current_gen)
        off1, off2 = crossover(parents[0], parents[1])
        new_population.append(off2)
        new_population.append(off1)
    for offspring in new_population:
        mutation(offspring, mutation_rate)
    next_gen.set_population(new_population)
    elite(old_population=current_gen, new_population=next_gen, elite_size=ELITE_SIZE)
    return next_gen


if __name__ == '__main__':
    # initialize population
    cities = init_cities(np.loadtxt(sys.argv[1]))
    start = timer()
    generation_count = 0
    population = Population(POPULATION_SIZE, cities)
    file_name = f"result-{start}.txt"
    file_result = f"final_result-{start}.txt"
    file = open(file_name, "w+")
    res_file = open(file_result, "w+")
    fittest = float('inf')
    best_gen = 0
    idx = population.get_worst_index()
    start_dis = population.get_fittest().distance
    file.write(
        f"Try with - Population size - {POPULATION_SIZE}, Mutation rate - {MUTATION_RATE}, Elite size - {ELITE_SIZE}, "
        f"Generation number - {NUMBER_OF_GENERATIONS}\n")
    file.write(f"Generation count: {generation_count} fittest: {population.get_fittest().distance}\n"
               f"route - {population.get_fittest().route}\n "
               f"the worst distance is: {population.population[idx].distance}\n")
    for i in range(NUMBER_OF_GENERATIONS):
        # print(f"Started generation {generation_count}")
        population = new_gen(population, MUTATION_RATE, cities)
        if fittest > population.get_fittest().distance:
            fittest = population.get_fittest().distance
            best_gen = generation_count
        generation_count += 1
    idx = population.get_worst_index()
    file.write(f"Generation count: {generation_count} fittest: {population.get_fittest().distance}\n"
               f"route - {population.get_fittest().route}\n "
               f"the worst distance is: {population.population[idx].distance}\n")
    end = timer()
    file.write(f"Shortest distance is {fittest} in generation {best_gen}\n"
               f"GA improved in {start_dis - fittest}\n")
    file.write(f"Program ran in {end - start} seconds\n")
    for c in population.get_fittest().route:
        res_file.write(f"{c.id}\n")
    file.close()
    res_file.close()
