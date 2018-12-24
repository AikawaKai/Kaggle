import pandas as pd
import sympy
import math


def main():
    cities = pd.read_csv("./data/cities.csv")
    tour = pd.read_csv("./submission_concorde1.csv")
    ids = cities["CityId"]
    primes = [p for p in sympy.primerange(0, len(ids))]

    arr = dict()
    all_x = cities["X"]
    all_y = cities["Y"]
    for i, id in enumerate(cities["CityId"]):
        arr[id] = (all_x[i], all_y[i])
    score = 0.0
    s = tour["Path"].values
    with open("./data/tour_distances1.csv", "w") as tour_dist:
        tour_dist.write("Path, dist, is_prime, needs_to_be_prime\n")
        tour_dist.write("0, 0, 0, 0\n")
        for i in range(0, len(s) - 1):
            p1 = arr[s[i]]
            p2 = arr[s[i + 1]]
            stepSize = math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))
            if s[i + 1] in primes:
                r = "1"
            else:
                r = "0"
            if ((i + 1) % 10 == 0) and (s[i] not in primes):
                stepSize *= 1.1
                tour_dist.write(str(s[i + 1]) + "," + str(stepSize) + "," + r + ",1\n")
            elif ((i + 1) % 10 == 0) and (s[i] in primes):
                tour_dist.write(str(s[i + 1]) + "," + str(stepSize) + "," + r + ",1\n")
            else:
                tour_dist.write(str(s[i + 1]) + "," + str(stepSize) + "," + r + ",0\n")
            # print(stepSize)
            score += stepSize
    print(score)

main()