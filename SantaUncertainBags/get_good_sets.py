from SantaUncertainBags.presents_dists import dict_
import random
import json


def get_random_config(n, max_int_for_toy):
    configs = []
    toys = list(dict_.keys())
    while n > 0:
        curr_dict = {}
        random.shuffle(toys)
        curr_toys = toys[:random.randint(0, len(toys))]
        for toy in curr_toys:
            curr_val = random.randint(0, max_int_for_toy[toy])
            if curr_val > 0:
                curr_dict[toy] = curr_val
        configs.append(curr_dict)
        n -= 1
    return configs


def get_good_config(n=100):
    pass


max_int_for_toy = {}
for toy in dict_.keys():
    curr_sum = 0
    i = 0
    while curr_sum < 50:
        curr_sum += dict_[toy]()
        i += 1
    max_int_for_toy[toy] = i

print(max_int_for_toy)


objects = dict_.keys()
configs = get_random_config(1000, max_int_for_toy)
num_trial = 1000
results = []
for j, config in enumerate(configs):  # configurazioni
    curr_config = []
    for i in range(0, num_trial):  # trials
        curr_sum = 0
        for toy, value in config.items():  # singoli toy nella configurazione
            for k in range(value):
                curr_sum += dict_[toy]()
        if curr_sum > 50:
            curr_sum = 0
        curr_config.append(curr_sum)
    results.append([config, sum(curr_config)/num_trial])
    print(j)
print(results)
print(len(results))
results = sorted(results, key=lambda x: x[1], reverse=True)
print(results)
results_as_string = []
with open('data.json') as f:
    data_json = json.load(f)
for dict_config, score in results:
    if score > 40:
        key_values = []
        for key, value in dict_config.items():
            key_values.append([key, value])
        key_values = sorted(key_values, key=lambda x: x[0])
        key_string = "_".join([name + "_" + str(v) for name, v in key_values])
        data_json[key_string] = score


print(len(data_json))
key_score = sorted([(key, score) for key, score in data_json.items()], key=lambda x: x[1], reverse=True)
with open('data.json', 'w') as fp:
    json.dump(data_json, fp)
