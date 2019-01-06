from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from numpy import isnan
from numpy import nan
from sklearn.model_selection import GridSearchCV
import sys

def get_new_x(X, set_year=None, set_month=None):
    col_0 = [str(v[0]).split("-")  for v in X]

    year = [v[0] if len(v)>1 else "2018" for v in col_0]
    month = [v[1] if len(v) > 1 else "12" for v in col_0]
    if set_year is None:
        set_year = {k: i for i, k in enumerate(set(year))}
    print(set_year)
    if set_month is None:
        set_month = {k: i for i, k in enumerate(set(month))}
    year_f = [set_year[v] for v in year]
    month_f = [set_month[v] for v in month]
    print(year_f)
    print(month_f)

    X_n = []
    for i, x in enumerate(X):
        new_x = list(x)[1:]
        new_x = [year_f[i], month_f[i]] + new_x
        X_n.append(new_x)
    return X_n, set_year, set_month


def get_counter_x(ids, X, trans_counter):
    new_X = []
    for i, x in enumerate(X):
        curr_id = ids[i]
        count = trans_counter[trans_counter["ids"] == curr_id]["counter"].values[0]
        new_x = list(x) + [count]
        new_X.append(new_x)
    return new_X


def main():
    train = pd.read_csv("./data/train.csv", sep=",")
    test = pd.read_csv("./data/test.csv", sep=",")
    trans_counter = pd.read_csv("./data/trans_counter.csv", sep=",")
    regr = RandomForestRegressor(max_depth=2, random_state=0,
                                 n_estimators=100)

    y = train["target"].values
    print(train.keys())
    print(y)
    X = train.iloc[:, [0, 2, 3, 4]].values
    print(X)
    id_train = train.iloc[:, 1].values
    X, set_year, set_month = get_new_x(X)


    X = get_counter_x(id_train, X, trans_counter)

    clf = GridSearchCV(RandomForestRegressor(),
                       {"max_depth":[1, 2, 3, 4], "random_state":[0],
                        "n_estimators": [5, 10, 20, 50, 100]}, cv=5)
    clf.fit(X, y)

    id_test = test.iloc[:, 1].values
    X_test = test.iloc[:, [0, 2, 3, 4]].values
    print(X_test)
    X_test, set_year, set_month = get_new_x(X_test, set_year, set_month)
    X_test = get_counter_x(id_test, X_test, trans_counter)
    y_test = clf.predict(X_test)

    print(y_test)
    print(id_test)
    dict_ = {"card_id": id_test, "target": y_test}
    pd.DataFrame.from_dict(dict_).to_csv("./first_submission1.csv", sep=",", index=False)


main()
