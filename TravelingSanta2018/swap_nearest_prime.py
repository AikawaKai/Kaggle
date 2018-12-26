import pandas as pd
import math
import sympy


def step_size(p1, p2):
    return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))


def try_swap_a(cities, tour, after, row, i):
    city_p_1 = cities[cities["CityId"] == tour.iloc[i - 1, 0]].values[0][1:]
    curr_city = cities[cities["CityId"] == tour.iloc[i, 0]].values[0][1:]  # swapped
    city_n_1 = cities[cities["CityId"] == tour.iloc[i+1, 0]].values[0][1:]  # swapped
    city_n_2 = cities[cities["CityId"] == tour.iloc[i+2, 0]].values[0][1:]
    dist_1 = step_size(city_p_1, curr_city)
    dist_2 = step_size(curr_city, city_n_1) * 1.1
    dist_3 = step_size(city_n_1, city_n_2)
    print(dist_1, dist_2, dist_3)
    old_dist = dist_1 + dist_2 + dist_3

    new_dist_1 = step_size(city_p_1, city_n_1)
    new_dist_2 = step_size(city_n_1, curr_city)
    new_dist_3 = step_size(curr_city, city_n_2)
    new_dist = new_dist_1 + new_dist_2 + new_dist_3
    prime = tour.iloc[i + 1, 0]
    not_prime = tour.iloc[i, 0]
    if old_dist-new_dist > 0:
        tour.iloc[i + 1] = not_prime
        tour.iloc[i] = prime
        new_tour = {"Path": tour["Path"]}
        pd.DataFrame.from_dict(new_tour).to_csv("./data/test.csv", sep=",", index=False)
    return old_dist-new_dist


def try_swap_b(cities, tour, before, row, i):
    city_p_2 = cities[cities["CityId"] == tour.iloc[i-2, 0]].values[0][1:]
    city_p_1 = cities[cities["CityId"] == tour.iloc[i-1, 0]].values[0][1:]  # swapped
    curr_city = cities[cities["CityId"] == tour.iloc[i, 0]].values[0][1:]  # swapped
    city_n_1 = cities[cities["CityId"] == tour.iloc[i+1, 0]].values[0][1:]
    #print(sympy.isprime(tour.iloc[i-1, 0]))
    dist_1 = step_size(city_p_2, city_p_1)
    dist_2 = step_size(city_p_1, curr_city)
    dist_3 = step_size(curr_city, city_n_1) * 1.1
    print(dist_1, dist_2, dist_3)
    old_dist = dist_1 + dist_2 + dist_3

    new_dist_1 = step_size(city_p_2, curr_city)
    new_dist_2 = step_size(curr_city, city_p_1)
    new_dist_3 = step_size(city_p_1, city_n_1)
    new_dist = new_dist_1 + new_dist_2 + new_dist_3
    prime = tour.iloc[i-1, 0]
    not_prime = tour.iloc[i, 0]
    if old_dist-new_dist>0:
        tour.iloc[i - 1] = not_prime
        tour.iloc[i] = prime
        new_tour = {"Path": tour["Path"]}
        pd.DataFrame.from_dict(new_tour).to_csv("./data/test.csv", sep=",", index=False)
        # pass
    return old_dist - new_dist


def swap(cities, tour, i, row):
    print(tour.iloc[i])
    before = tour.iloc[i-1, :]
    after = tour.iloc[i+1, :]
    dist = tour.iloc[i, 1]
    dist_before = tour.iloc[i-1, 1]
    dist_after = tour.iloc[i+1, 1]
    dist_after_after = tour.iloc[i+2, 1]
    print(dist_before, dist, dist_after)
    print(dist, dist_after, dist_after_after)
    dist1 = dist_before + dist + dist_after  # dist for before
    dist2 = dist + dist_after + dist_after_after  # dist for after
    print(dist1, dist2)
    gain1 = 0
    gain2 = 0
    if int(before[2]) == 1:
        print("Before is prime")
        dist_1_b = try_swap_b(cities, tour, before, row, i)
    if int(after[2]) == 1:
        print("After is prime")
        print(after)
        dist_1_a = try_swap_a(cities, tour, after, row, i)


def main():
    cities = pd.read_csv("./data/cities.csv")
    tour = pd.read_csv("./data/tour_distances1.csv")
    """
    print(tour.keys())
    print(tour["needs_to_be_prime"])
    tour["needs_to_be_prime"] = list([int(v) for v in tour["needs_to_be_prime"]])
    tour.to_csv("./data/tour_distances1.csv", sep=",", index=False)
    """
    for i in range(1, len(tour)):
        row = tour.iloc[i-1]
        if i % 10 == 0:
            if int(row[2]) == 0:
                print()
                print("##########")
                swap(cities, tour, i-1, row)

main()