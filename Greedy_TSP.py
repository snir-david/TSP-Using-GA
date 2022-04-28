import sys
import numpy as np
from classes import City


def init_cities(cities_list):
    cities = []
    for i in range(len(cities_list)):
        c = City(cities_list[i][0], cities_list[i][1], i)
        cities.append(c)
    return cities


def distance(city1, city2):
    xDis = abs(city1.x - city2.x)
    yDis = abs(city1.y - city2.y)
    distance = np.sqrt((xDis ** 2) + (yDis ** 2))
    return distance


def find_closest_city(current_city, cities_left):
    min_dist = float('inf')
    closest_city = None
    for city in cities_left:
        dist = distance(current_city, city)
        if dist < min_dist:
            min_dist = dist
            closest_city = city
    return closest_city, min_dist


if __name__ == '__main__':
    for i in range(1,48):
        orig_cities = init_cities(np.loadtxt(sys.argv[1]))
        file_name = f"greedy-city-{i}.txt"
        file = open(file_name, "+w")
        file.write(f"Starting from city - {i}\n")
        cities = orig_cities
        route = []
        distances = []
        first_city = cities[i]
        current = first_city
        route.append(current)
        cities.remove(current)
        for j in range(len(cities) - 1):
            city, dist = find_closest_city(current, cities)
            current = city
            route.append(city)
            distances.append(dist)
            cities.remove(city)
        current = cities[0]
        total_dist = 0
        for x in distances:
            total_dist += x
        total_dist += distance(first_city, current)
        file.write(f"Total distance from city {i} is {total_dist}\n")
        for c in route:
            file.write(f"{c.id} ")
