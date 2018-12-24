import pandas as pd
from math import sqrt
import sympy


def add_prime_to_csv_file(tour_dist):
    start_prime = []
    end_prime = []
    for index, row in tour_dist.iterrows():
        # print(index, row.values)
        if sympy.isprime(int(row["start"])):
            start_prime.append(1)
        else:
            start_prime.append(0)
        if sympy.isprime(int(row["end"])):
            end_prime.append(1)
        else:
            end_prime.append(0)

    print(start_prime)
    print(end_prime)
    dict_ = {"start": tour_dist["start"], "end": tour_dist["end"], "dist": tour_dist["dist"],
             "start_needs_to_be_prime": tour_dist["start_needs_to_be_prime"], "start_is_prime": start_prime,
             "end_is_prime": end_prime}

    pd.DataFrame.from_dict(dict_).to_csv("./data/tour_distances1.csv", sep=",", index=False)


class Path(object):

    def __init__(self, cities, start_city_id, end_city_id):
        self.cities = cities
        self.start_id = start_city_id
        self.end_id = end_city_id
        self._calculate_dist()

    def _calculate_dist(self):
        start_city = self.cities[self.cities["CityId"] == self.start_id]
        end_city = self.cities[self.cities["CityId"] == self.end_id]
        x_1 = start_city["X"].values[0]
        y_1 = start_city["Y"].values[0]

        x_2 = end_city["X"].values[0]
        y_2 = end_city["Y"].values[0]
        self.distance = euclidean_distance(x_1, x_2, y_1, y_2)

    def get_dist(self):
        return self.distance


def euclidean_distance(x1, x2, y1, y2):
    return sqrt(pow(x1-x2, 2) + pow(y1-y2, 2))


def swap(cities, tour_dist, curr_prime_index, curr_possible_position):
    city_prime = tour_dist.iloc[curr_prime_index, 0]
    previous_city_prime = tour_dist.iloc[curr_prime_index - 1, 0]
    next_city_prime = tour_dist.iloc[curr_prime_index, 1]
    # path city prime and previous
    dist_prime_1 = tour_dist.iloc[curr_prime_index - 1, 2]
    dist_prime_2 = tour_dist.iloc[curr_prime_index, 2]
    dist_prime = dist_prime_1 + dist_prime_2
    print("\n###############")
    print("Prime not in position")
    print(previous_city_prime, "[", city_prime, "]", dist_prime_1)
    print("[", city_prime, "]", next_city_prime, dist_prime_2)

    city_not_in_position = tour_dist.iloc[curr_possible_position, 0]
    previous_city_not_in_position = tour_dist.iloc[curr_possible_position-1, 0]
    next_city_not_in_position = tour_dist.iloc[curr_possible_position, 1]
    # path city not in position
    dist_pos_1 = tour_dist.iloc[curr_possible_position - 1, 2]
    dist_pos_2 = tour_dist.iloc[curr_possible_position, 2]
    dist_pos = dist_pos_1 + dist_pos_2
    print("City not in position")
    print(previous_city_not_in_position, "[", city_not_in_position, "]", dist_pos_1)
    print("[", city_not_in_position, "]", next_city_not_in_position, dist_pos_2)

    # print("curr_dist", dist_prime + dist_pos)

    # swap
    path1 = Path(cities, previous_city_prime, city_not_in_position)
    path2 = Path(cities, city_not_in_position, next_city_prime)

    path3 = Path(cities, previous_city_not_in_position, city_prime)
    path4 = Path(cities, city_prime, next_city_not_in_position)
    # print(path1.get_dist(), path2.get_dist(), path3.get_dist(), path4.get_dist())
    new_dist = path1.get_dist()+path2.get_dist()+path3.get_dist()+path4.get_dist()
    # print("new dist", new_dist)
    improvement = dist_prime + dist_pos - new_dist
    # print("Improvement", improvement)
    if improvement > 0:
        apply_swap(tour_dist, curr_prime_index, curr_possible_position,
                   city_prime,
                   city_not_in_position,
                   path1, path2, path3, path4)
    return improvement


def apply_swap(tour_dist, curr_prime_index, curr_possible_position ,
               city_prime,
               city_not_in_position,
               path1, path2, path3, path4):

    tour_dist.iloc[curr_prime_index, 0] = city_not_in_position
    tour_dist.iloc[curr_prime_index, 4] = 0
    tour_dist.iloc[curr_prime_index-1, 1] = city_not_in_position
    tour_dist.iloc[curr_prime_index - 1, 5] = 0
    tour_dist.iloc[curr_prime_index-1, 2] = path1.get_dist()
    tour_dist.iloc[curr_prime_index, 2] = path2.get_dist()

    tour_dist.iloc[curr_possible_position, 0] = city_prime
    tour_dist.iloc[curr_possible_position, 4] = 1
    tour_dist.iloc[curr_possible_position-1, 1] = city_prime
    tour_dist.iloc[curr_possible_position-1, 5] = 1
    tour_dist.iloc[curr_possible_position-1, 2] = path3.get_dist()
    tour_dist.iloc[curr_possible_position, 2] = path4.get_dist()
    print("-------------------------------------------------", city_not_in_position, city_prime)
    tour_dist.to_csv("./data/tour_distances1_1.csv", sep=",", index=False)

def main():
    tour_dist = pd.read_csv("./data/tour_distances1.csv")
    cities = pd.read_csv("data./cities.csv")
    print(tour_dist.keys())
    # add_prime_to_csv_file(tour_dist)
    index_prime_end_not_in_position = []
    for index, row in tour_dist.iterrows():
        if int(row["start_is_prime"]) == 1 and int(row["start_needs_to_be_prime"]) == 0:
            index_prime_end_not_in_position.append(index)

    index_position_not_filled_correctly = []
    for index, row in tour_dist.iterrows():
        if int(row["start_needs_to_be_prime"]) == 1 and int(row["start_is_prime"]) == 0:
            index_position_not_filled_correctly.append(index)

    print(index_position_not_filled_correctly)
    print(index_prime_end_not_in_position)

    while len(index_prime_end_not_in_position) > 0:
        curr_prime_index = index_prime_end_not_in_position[0]
        index_prime_end_not_in_position = index_prime_end_not_in_position[1:]
        improvement = 0
        i = 0
        while improvement <= 0 and i < 100:
            curr_possible_position = index_position_not_filled_correctly[i]
            improvement = swap(cities, tour_dist, curr_prime_index, curr_possible_position)
            if improvement > 0:
                del index_position_not_filled_correctly[i]
                print("improvement", improvement)
            else:
                i += 1

main()