import pandas as pd
import sympy

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
         "end_need_to_be_prime": tour_dist["end_need_to_be_prime"], "start_is_prime": start_prime,
         "end_is_prime": end_prime}

pd.DataFrame.from_dict(dict_).to_csv("./data/tour_distances1.csv", sep=",", index=False)
"""
print(tour_dist.keys())

index_prime_end_not_in_position = []
for index, row in tour_dist.iterrows():
    if int(row["end_is_prime"]) == 1 and int(row["end_need_to_be_prime"]) == 0:
        index_prime_end_not_in_position.append(index)


print(len(index_prime_end_not_in_position))


index_position_not_filled_correctly = []
for index, row in tour_dist.iterrows():
    if int(row["end_need_to_be_prime"]) == 1 and int(row["end_is_prime"]) == 0:
        index_position_not_filled_correctly.append(index)

print(len(index_position_not_filled_correctly))



