from SantaUncertainBags.presents_dists import dict_
import json
import pandas as pd
import random


def shuffle_best(data):
    data_40 = [d for d in data if d[1] >= 35]
    data_35 = [d for d in data if 35 > d[1] >= 30]
    data_30 = [d for d in data if 30 > d[1] >= 25]
    data_other = [d for d in data if d[1] < 25]
    random.shuffle(data_40)
    random.shuffle(data_35)
    new_data = data_40 + data_35 + data_30 + data_other
    return new_data


def int_value_from_key(key):
    values = key.split("_")
    int_value = [int(values[i]) for i in range(1, len(values), 2)]
    return sum(int_value)


def get_num_toys(key):
    values = key.split("_")
    return len(values)//2


def config_usable2(config):
    values = config.split("_")
    values = [(values[i], values[i + 1]) for i in range(0, len(values), 2)]
    config = values
    if sum([int(v) for k, v in config]) < 3:
        return False
    return True


def config_usable(config, toys_dict):
    if sum([int(v) for k, v in config]) <3:
        return False
    for key, value in config:
        if len(toys_dict[key]) >= int(value):
            continue
        else:
            return False
    return True


def get_values_from_config(config, toys_dict):
    toys = []
    for key, value in config:
        list_ = toys_dict[key]
        toys += list_[:int(value)]
        toys_dict[key] = list_[int(value):]
    return toys


def is_dict_empty(dict_):
    tot = 0
    for key, list_ in dict_.items():
        tot += len(list_)
    return tot == 0


def get_last_row(toys):
    row = []
    for key, value in toys.items():
        row += value
        toys[key] = []
    return row

with open('data.json') as f:
    data_json = json.load(f)


gifts = pd.read_csv("data/gifts.csv")["GiftId"]
toys_dict = {}
for gift in gifts:
    gif = gift.split("_")[0]
    if gif not in toys_dict:
        toys_dict[gif] = [gift]
    else:
        toys_dict[gif].append(gift)

for toy, value in toys_dict.items():
    random.shuffle(value)

sorted_best = sorted([(key, score) for key, score in data_json.items()], key=lambda x: x[1],
                     reverse=True)
sorted_best = list(filter(lambda x: config_usable2(x[0]), sorted_best))
sorted_best = shuffle_best(sorted_best)

#random.shuffle(sorted_best)
rows = []
i = 0
while not is_dict_empty(toys_dict) and i < len(sorted_best):
        key, score = sorted_best[i]
        values = key.split("_")
        values = [(values[i], values[i+1]) for i in range(0, len(values), 2)]
        j = 0
        while config_usable(values, toys_dict) and len(rows) < 999:
            config_values = get_values_from_config(values, toys_dict)
            rows.append(config_values)
            j += 1
        print(is_dict_empty(toys_dict))
        print(len(rows))
        i += 1
        if len(rows) >= 999:
            last_row = get_last_row(toys_dict)
            rows.append(last_row)

with open("submission.csv", "w") as f:
    f.write("Gifts\n")
    for row in rows:
        curr_row = "\t".join(row)+"\n"
        f.write(curr_row)


