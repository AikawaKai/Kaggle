import pandas as pd
from random import randint
import math


def euclidean_dist(cities, city1, city2):
    p1 = cities[cities["CityId"] == city1].values[1:]
    p2 = cities[cities["CityId"] == city2].values[1:]
    stepSize = math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))
    return stepSize


def info_city(tour, index, len_):
    city = tour.iloc[index, 0]
    city_is_prime = tour.iloc[index, 2]
    city_pos_needs_to_be_prime = tour.iloc[index, 3]
    index_prev = index-1 if index > 0 else len_
    prev_city = tour.iloc[index_prev, 0]
    index_next = index+1 if index < len_ else 0
    next_city = tour.iloc[index_next, 0]
    curr_dist_from_city = tour.iloc[index_next, 1] + tour.iloc[index, 1]
    return city, city_is_prime, city_pos_needs_to_be_prime, prev_city, next_city, curr_dist_from_city


def swap(cities, tour, index1, index2, len_):
    res1 = info_city(tour, index1, len_)
    city1, city_is_prime1, city_pos_needs_to_be_prime1, prev_city1, next_city1, curr_dist_from_city1 = res1

    res2 = info_city(tour, index2, len_)
    city2, city_is_prime2, city_pos_needs_to_be_prime2, prev_city2, next_city2, curr_dist_from_city2 = res2

    curr_tot_distance = curr_dist_from_city1 + curr_dist_from_city2
    print("Current tot distance:", curr_tot_distance)



if __name__ == '__main__':
    tour = pd.read_csv("./data/tour_distances1.csv")
    cities = pd.read_csv("./data/cities.csv")

    path = tour["Path"].values
    len_ = len(path)-1
    while True:
        index1 = randint(0, len_)
        index2 = randint(0, len_)
        swap(cities, tour, index1, index2, len_)
