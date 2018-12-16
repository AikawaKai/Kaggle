import pandas as pd
import numpy
import time


cities = pd.read_csv("data/cities.csv")
CityId = list(cities["CityId"])
x = list(cities["X"])
y = list(cities["Y"])

print(len(x))
cities_x_y = list(zip(CityId, x, y))
i = 0
for id_1, x_1, y_1 in cities_x_y:
    a = numpy.array((x_1, y_1))
    i += 1
    start = time.time()
    for id_2, x_2, y_2 in cities_x_y:
        b = numpy.array((x_2, y_2))
        numpy.linalg.norm(a - b)
        i += 1
    end = time.time()
    print(end-start)

print(i)