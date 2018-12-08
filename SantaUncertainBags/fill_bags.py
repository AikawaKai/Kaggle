from SantaUncertainBags.presents_dists import dict_
from numpy import mean, std
import sys
import pandas as pd
from collections import Counter

presents = ["horse", "ball", "bike", "train", "coal", "book", "doll", "block", "gloves"]


def get_sample(present, num):
    sample = []
    while num > 0:
        sample.append(dict_[present]())
        num -= 1
    return sample


samples_n = []
for present in presents:
    print(present)
    sample = get_sample(present, 100)
    samples_n.append((present, mean(sample), std(sample), max(sample)))
print(samples_n)

path_ = sys.argv[1]
gifts_df = pd.read_csv(path_ + "\\" + "gifts.csv")
gifts = list(gifts_df["GiftId"])
gifts = Counter([val.split("_")[0] for val in gifts])