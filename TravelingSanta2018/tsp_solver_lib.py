import pandas as pd
import numpy
import time
import random

cities = pd.read_csv("data/cities.csv")
CityId = list(cities["CityId"])
x = list(cities["X"])
y = list(cities["Y"])