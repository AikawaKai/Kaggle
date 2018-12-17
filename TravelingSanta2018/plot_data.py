import matplotlib.pyplot as plt
import pandas as pd


cities = pd.read_csv("data/cities.csv", delimiter=",")
citiesId = cities["CityId"]
x = list(cities["X"])
y = list(cities["Y"])
print(x, y)
plt.scatter(x, y, s=0.01)
plt.show()
