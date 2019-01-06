import pandas as pd

transac = "./data/historical_transactions.csv"
new_transac = "./data/new_merchant_transaction.csv"
train = pd.read_csv("./data/train.csv", sep=",")
test = pd.read_csv("./data/test.csv", sep=",")

train_card_id = list(train["card_id"].values)
test_card_id = list(test["card_id"].values)
tot_id = train_card_id + test_card_id
dict_id = {id_: 0 for id_ in tot_id}
print(dict_id)
with open(transac, "r") as transac_open:
    first = next(transac_open)
    for line in transac_open:
        curr_id = line.split(",")[1]
        dict_id[curr_id] += 1
ids_counter = dict_id.items()
ids = [id_ for id_, counter in ids_counter]
counter = [c for id_, c in ids_counter]
dict_to_csv = {"ids": ids, "counter": counter}
pd.DataFrame.from_dict(dict_to_csv).to_csv("./data/trans_counter.csv", sep=",", index=False)