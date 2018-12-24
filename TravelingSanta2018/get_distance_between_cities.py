import pandas as pd
import sys
from math import sqrt


def euclidean_distance(x1, x2, y1, y2):
    return sqrt(pow(x1-x2, 2) + pow(y1-y2, 2))


cities = pd.read_csv("./data/cities.csv", sep=",")
city1 = int(sys.argv[1])
city2 = int(sys.argv[2])
x1 = cities[cities["CityId"] == city1]["X"].values[0]
x2 = cities[cities["CityId"] == city2]["X"].values[0]

y1 = cities[cities["CityId"] == city1]["Y"].values[0]
y2 = cities[cities["CityId"] == city2]["Y"].values[0]

print(euclidean_distance(x1, x2, y1, y2))