from SantaUncertainBags.presents_dists import dict_
from numpy import mean, std
import sys
import pandas as pd
from collections import Counter
from copy import deepcopy

presents = ["horse", "ball", "bike", "train", "coal", "book", "doll", "blocks", "gloves"]


def my_sum(values):
    sum_ = 0
    for n, v in values:
        sum_ += v
    return sum_


def get_sample(present, num):
    sample = []
    while num > 0:
        sample.append(dict_[present]())
        num -= 1
    return sample


def sort_by_lighter(samples_n):
    return sorted(samples_n, key=lambda x: x[1]+x[2])


def greedy_selection(all_items, num_gifts):
    curr_val = all_items.pop(len(all_items)-1)
    curr_bag = [curr_val]
    num_gifts -= 1
    while num_gifts > 0 and my_sum(curr_bag) < 49:
        curr_bag.append(all_items.pop(0))
        num_gifts -= 1
    return curr_bag, num_gifts




samples_n = []
for present in presents:
    print(present)
    sample = get_sample(present, 100)
    samples_n.append([present, mean(sample), std(sample), max(sample), 0])
print(samples_n)


path_ = sys.argv[1]
gifts_df = pd.read_csv(path_ + "\\" + "gifts.csv")
gifts = list(gifts_df["GiftId"])
num_gifts = len(gifts)
gifts = Counter([val.split("_")[0] for val in gifts])
sorted_gifts_lighter = sort_by_lighter(samples_n)
all_items = []
for name, mean_, std_, max_, counter in sorted_gifts_lighter:
    curr_counter = gifts[name]
    all_items += [(name + "_" + str(k), mean_) for k in range(curr_counter)]
print(all_items)
j = 0
bags = []
while num_gifts > 0:
    curr_bag, num_gifts = greedy_selection(all_items, num_gifts)
    bags.append(curr_bag)
    print(len(bags), num_gifts)
print(bags)


print(len(bags))
with open("first.csv", "w") as submission:
    submission.write("Gifts\n")
    for bag in bags:
        line = "\t".join([bag[i][0] for i in range(len(bag))])
        submission.write(line+"\n")

print(gifts)
print(samples_n)