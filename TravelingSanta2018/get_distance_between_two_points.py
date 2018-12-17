import pandas as pd
import numpy
import time
import random


def dist(x, y):
    return numpy.sqrt(numpy.sum((x-y)**2))


cities = pd.read_csv("data/cities.csv")
CityId = list(cities["CityId"])
x = list(cities["X"])
y = list(cities["Y"])

print(len(x))
cities_x_y = list(zip(CityId, x, y))
i = 0
already_been_there = {}
all_set = {id: (x, y) for id, x, y in cities_x_y}

first_index = 0
first_city = all_set[first_index]
all_set.pop(first_index, None)
print(first_index)
print(first_city)
random.shuffle(cities_x_y)
sets = [first_index]
print(sets)
shuffled_set = list(all_set.items())
random.shuffle(shuffled_set)
while len(all_set) > 0:
    # start = time.time()
    b = numpy.array((first_city[0], first_city[1]))
    shuffled_set = shuffled_set[:1000]
    distances = []
    for key, value in shuffled_set:
        a = numpy.array((value[0], value[1]))
        dist_a_b = dist(a, b)
        distances.append([key, dist_a_b, value[0], value[1]])
    distances = sorted(distances, key=lambda x: x[1])
    best = distances[0]
    sets.append(best[0])
    all_set.pop(best[0])
    first_city = (best[2], best[3])
    # end = time.time()
    # print(end - start)
    shuffled_set = list(all_set.items())


with open("submission.csv", "w") as f:
    f.write("Path\n")
    for line in sets:
        f.write(str(line)+"\n")