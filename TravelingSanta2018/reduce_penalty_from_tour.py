import pandas as pd
from math import sqrt
import sympy


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
    curr_prime_row = tour_dist.iloc[[curr_prime_index]]
    curr_position_row = tour_dist.iloc[[curr_possible_position]]

    # prime
    tot_dist_1 = 0
    prime_city_id = curr_prime_row["start"].values[0]
    end_city_id = curr_prime_row["end"].values[0]
    dist_1 = curr_prime_row["dist"].values[0]
    tot_dist_1 += dist_1

    previous_to_prime = tour_dist.iloc[[curr_prime_index-1]]
    previous_start_city_id = previous_to_prime["start"].values[0]
    previous_end_city_id = previous_to_prime["end"].values[0] # this is prime
    dist_1_2 = previous_to_prime["dist"].values[0]
    tot_dist_1 += dist_1_2

    # position
    tot_dist_2 = 0
    start_pos_city_id = curr_position_row["start"].values[0]
    end_pos_city_id = curr_position_row["end"].values[0]
    dist_2 = curr_position_row["dist"].values[0]
    tot_dist_2 += dist_2

    previous_to_position = tour_dist.iloc[[curr_possible_position-1]]
    previous_start_city_pos_id = previous_to_position["start"].values[0]
    previous_end_city_pos_id = previous_to_position["end"].values[0] # this is the same as end_pos_city_id
    dist_2_2 = previous_to_position["dist"].values[0]
    tot_dist_2 += dist_2_2

    path1 = Path(cities, start_pos_city_id, end_city_id)
    path2 = Path(cities, previous_start_city_id, start_pos_city_id)

    path3 = Path(cities, prime_city_id, end_pos_city_id)
    path4 = Path(cities, previous_start_city_id, prime_city_id)
    new_dist = path1.get_dist()+path2.get_dist()+path3.get_dist()+path4.get_dist()
    #print("old dist", tot_dist_1 + tot_dist_2, "new dist", new_dist)
    if tot_dist_1 + tot_dist_2 - new_dist > 0:
        swap_tour(tour_dist, curr_prime_index, curr_possible_position, path1, path2, path3, path4, prime_city_id,
                  start_pos_city_id)
    return tot_dist_1+tot_dist_2-new_dist


def swap_tour(tour_dist, prime_row_index, position_row_index, path1, path2, path3, path4, prime_city_id,
              start_pos_city_id):
    print(prime_city_id, start_pos_city_id)
    tour_dist.iloc[prime_row_index, 0] = start_pos_city_id
    tour_dist.iloc[prime_row_index, 2] = path1.get_dist()
    tour_dist.iloc[prime_row_index, 5] = 0

    tour_dist.iloc[prime_row_index-1, 1] = start_pos_city_id
    tour_dist.iloc[prime_row_index-1, 2] = path2.get_dist()
    tour_dist.iloc[prime_row_index-1, 4] = 0
    print(position_row_index, prime_row_index)
    tour_dist.iloc[position_row_index, 0] = prime_city_id
    tour_dist.iloc[position_row_index, 2] = path3.get_dist()
    tour_dist.iloc[position_row_index, 5] = 1

    tour_dist.iloc[position_row_index-1, 1] = prime_city_id
    tour_dist.iloc[position_row_index-1, 2] = path4.get_dist()
    tour_dist.iloc[position_row_index-1, 4] = 1

    tour_dist.to_csv("./data/tour_distances1_1.csv", sep=",", index=False)


def main():
    tour_dist = pd.read_csv("./data/tour_distances1.csv")
    cities = pd.read_csv("data./cities.csv")

    """
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
    print(tour_dist.keys())
    """

    tour_dist["start_needs_to_be_prime"] = [0]+list(tour_dist["start_needs_to_be_prime"])[:-1]
    index_prime_end_not_in_position = []
    for index, row in tour_dist.iterrows():
        if int(row["start_is_prime"]) == 1 and int(row["start_needs_to_be_prime"]) == 0:
            index_prime_end_not_in_position.append(index)

    index_position_not_filled_correctly = []
    for index, row in tour_dist.iterrows():
        if int(row["start_needs_to_be_prime"]) == 1 and int(row["start_is_prime"]) == 0:
            index_position_not_filled_correctly.append(index)

    print(index_position_not_filled_correctly)
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