import pandas as pd
import sympy
from math import sqrt


def euclidean_distance(x1, x2, y1, y2):
    return sqrt(pow(x1-x2, 2) + pow(y1-y2, 2))


def get_distance(df_cities, couple):
    index1, index2 = couple
    city1 = df_cities[df_cities["CityId"] == index1]
    city2 = df_cities[df_cities["CityId"] == index2]
    city1_x = city1["X"].values
    city1_y = city1["Y"].values
    city2_x = city2["X"].values
    city2_y = city2["Y"].values
    return euclidean_distance(city1_x, city2_x, city1_y, city2_y)


def get_distances(df_cities, df_tour):
    path = list(df_tour["Path"])
    couples = [(path[i], path[i+1]) for i in range(0, len(path)-1)]
    distances = [(get_distance(df_cities, coup), coup) for coup in couples]
    return distances


def get_increment(distances):
    new_distances = [distances[0]]
    for i, (d, (start, end)) in enumerate(distances[1:]):
        if i % 10 == 0:
            if not sympy.isprime(end):
                new_distances.append([d*1.1, (start, end)])
            else:
                new_distances.append([d, (start, end)])
        else:
            new_distances.append([d, (start, end)])
    return new_distances


def main():
    cities = pd.read_csv("./data/cities.csv")
    tour = pd.read_csv("./submission_concorde1.csv")
    ids = cities["CityId"]
    # primes = [p for p in sympy.primerange(0, len(ids))]
    distances = get_distances(cities, tour)
    print(sum([d for d, couple in distances]))
    incremented_distances = get_increment(distances)
    with open("./data/tour_distances1.csv", "w") as tour_dist:
        tour_dist.write("start,end,dist,end_need_to_be_prime\n")
        for i, (d, (start, end)) in enumerate(incremented_distances):
            if (i % 10) == 0:
                tour_dist.write(str(start) + "," + str(end) + "," + str(d) + ",1\n")
            else:
                tour_dist.write(str(start) + "," + str(end) + "," + str(d) + ",0\n")
    # distances_to_check = distances[9:-1:10]
    print(sum([d for d, couple in incremented_distances]))
    '''
    sum_ = 0
    for d, couple in distances:
        sum_ += d
    print(sum_+increment)
    '''

main()