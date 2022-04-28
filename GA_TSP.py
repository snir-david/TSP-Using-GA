import sys
from timeit import default_timer as timer
import matplotlib.pyplot as plt
from classes import *

POPULATION_SIZE = 300
ELITE_SIZE = int(POPULATION_SIZE * 0.1)
MUTATION_RATE = 10
NUMBER_OF_GENERATIONS = 5000


# drawing plot according to the num of iteration and loss cost
def draw_plot(fittest, average, generation_count, time):
    plt.plot(generation_count, fittest, label="Fittest")
    plt.plot(generation_count, average, label="Average")
    plt.legend()
    plt.xlabel("Generation")
    plt.ylabel("Distance")
    plt.savefig(f"Plot of {time}.png")
    plt.clf()


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
    # print(len(o1.route), len(o2.route), point)
    return o1, o2


def mutation(chromosome, mutation_rate: int):
    for idx in range(len(chromosome.route)):
        if random.randint(0, 100) < mutation_rate:
            idx2 = random.randint(0, len(chromosome.route) - 1)
            chromosome.swap(idx, idx2)


def weighted_selection(population):
    return random.choices(population=population.population, cum_weights=population.weights, k=POPULATION_SIZE)


def random_selection(population):
    parents = []
    for i in range(POPULATION_SIZE):
        parents.append(population.population[random.randint(0,POPULATION_SIZE-1)])
    return parents


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
    parents = weighted_selection(current_gen)
    i = 0
    for j in range(int(len(parents) / 2)):
        off1, off2 = crossover(parents[i], parents[i+1])
        new_population.append(off1)
        new_population.append(off2)
        mutation(off1, mutation_rate)
        mutation(off2, mutation_rate)
        i += 2
    next_gen.set_population(new_population)
    elite(old_population=current_gen, new_population=next_gen, elite_size=ELITE_SIZE)
    return next_gen


def main_func():
    start = timer()
    generation_count = 0
    average = []
    fittestList = []
    gen_count = []
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
    for generation_count in range(NUMBER_OF_GENERATIONS):
        # print(f"Started generation {generation_count}")
        population = new_gen(population, MUTATION_RATE, cities)
        gen_count.append(generation_count)
        fittestList.append(population.get_fittest().distance)
        average.append(population.get_average())
        if fittest > population.get_fittest().distance:
            fittest = population.get_fittest().distance
            best_gen = generation_count
    idx = population.get_worst_index()
    file.write(f"Generation count: {generation_count} fittest: {population.get_fittest().distance}\n"
               f"route - {population.get_fittest().route}\n "
               f"the worst distance is: {population.population[idx].distance}\n")
    end = timer()
    file.write(f"Shortest distance is {fittest} in generation {best_gen}\n"
               f"Average distance is {average[generation_count]}"
               f"GA improved in {start_dis - fittest}\n")
    file.write(f"Program ran in {end - start} seconds\n")
    for c in population.get_fittest().route:
        res_file.write(f"{c.id}\n")
    file.close()
    res_file.close()
    draw_plot(fittestList, average, gen_count, start)
    return fittest


if __name__ == '__main__':
    # initialize population
    cities = init_cities(np.loadtxt(sys.argv[1]))
    fit = 0
    num_of_try = 10
    for i in range(num_of_try):
        start = timer()
        print(f"Started GA in {start}")
        curr = main_func()
        fit += curr
        end = timer()
        print(f"GA Finish in {end - start} and the best distance is - {curr}")
    print(f"Average fittest - {fit / num_of_try}")
