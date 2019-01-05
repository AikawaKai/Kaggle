import pandas as pd
from itertools import permutations
from math import sqrt
from sympy import isprime


def get_dist(cities, city_1, city_2):
    city_1_x_y = cities[cities["CityId"] == city_1]
    city_2_x_y = cities[cities["CityId"] == city_2]
    city_1_x = city_1_x_y["X"].values[0]
    city_1_y = city_1_x_y["Y"].values[0]

    city_2_x = city_2_x_y["X"].values[0]
    city_2_y = city_2_x_y["Y"].values[0]
    return sqrt(pow(city_1_x - city_2_x, 2) + pow(city_1_y - city_2_y, 2))


def suboptimalpath(cities, sub_path):
    curr_dist = sum([get_dist(cities, sub_path[i], sub_path[i + 1]) * 1.1
                 if i == len(sub_path) - 2 and not isprime(sub_path[i + 1])
                 else get_dist(cities, sub_path[i], sub_path[i + 1])
                     for i in range(0, len(sub_path) - 1)])
    curr_best = curr_dist

    start = sub_path[0]
    end = sub_path[7:]
    to_perm = sub_path[1:7]
    perms = permutations(to_perm)
    for p in perms:
        curr_sub_path = [start] + list(p) + end
        curr_dist = sum([get_dist(cities, curr_sub_path[i], curr_sub_path[i + 1]) * 1.1
                         if i == len(curr_sub_path) - 2 and not isprime(curr_sub_path[i + 1])
                         else get_dist(cities, curr_sub_path[i], curr_sub_path[i + 1])
                         for i in range(0, len(curr_sub_path) - 1)])
        if curr_best-curr_dist > 0:
            print(curr_best-curr_dist)
            break
    print("done")

tour = pd.read_csv("./data/best.csv", sep=",")
cities = pd.read_csv("./data/cities.csv", sep=",")
print(tour)

print(cities.keys())
print(tour.keys())
path = list(tour["Path"])
print(path)

for i in range(0, len(path), 10):
    curr_sub_path = path[i:i+11]
    suboptimalpath(cities, curr_sub_path)

"""       
curr_sub_path = path[:11]
suboptimalpath(cities, curr_sub_path)
suboptimalpath(cities, path[10:10+11])
"""



