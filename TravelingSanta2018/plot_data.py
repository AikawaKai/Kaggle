import matplotlib.pyplot as plt
import pandas as pd
from math import sqrt


cities = pd.read_csv("data/cities.csv", delimiter=",")
citiesId = cities["CityId"]
x = list(cities["X"])
y = list(cities["Y"])
print(x, y)

plt.scatter(x, y, s=0.01)
plt.show()

_75721_x = x[75721]
_75721_y = y[75721]
_37147_x = x[37147]
_37147_y = y[37147]

print(sqrt((_75721_x - _37147_x) * (_75721_x - _37147_x) + (_75721_y - _37147_y) * (_75721_y - _37147_y)))