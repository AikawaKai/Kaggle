from SantaUncertainBags.presents_dists import dict_
from numpy import mean, std
import sys
import pandas as pd
from collections import Counter

presents = ["horse", "ball", "bike", "train", "coal", "book", "doll", "block", "gloves"]


def my_sum(values):
    sum_ = 0
    for n, v, k in values:
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


samples_n = []
for present in presents:
    print(present)
    sample = get_sample(present, 100)
    samples_n.append((present, mean(sample), std(sample), max(sample)))
print(samples_n)

path_ = sys.argv[1]
gifts_df = pd.read_csv(path_ + "\\" + "gifts.csv")
gifts = list(gifts_df["GiftId"])
num_gifts = len(gifts)
gifts = Counter([val.split("_")[0] for val in gifts])

sorted_gifts_lighter = sort_by_lighter(samples_n)
print(sorted_gifts_lighter)
i = 1000
j = 0
bags = []
while num_gifts > 0 and j < len(gifts):
    curr_gift = sorted_gifts_lighter[j]
    print(curr_gift)
    curr_type, curr_mean, curr_std, curr_max = curr_gift
    curr_counter = gifts[curr_type]
    print(curr_counter)
    curr_bag = []
    k = 0
    while curr_counter > 0:
        if my_sum(curr_bag) < 50:
            curr_bag.append((curr_type, curr_mean, k))
        else:
            bags.append(curr_bag)
            curr_bag = [(curr_type, curr_mean, k)]
            i -= 1

        curr_counter -= 1
        k += 1
        num_gifts -= 1
    j += 1
    print(j)

print(len(bags), i)
with open("first.csv", "w") as submission:
    submission.write("Gifts\n")
    for bag in bags:
        line = "\t".join([bag[i][0] + "_" + str(bag[i][2]) for i in range(len(bag))])
        submission.write(line+"\n")


print(samples_n)