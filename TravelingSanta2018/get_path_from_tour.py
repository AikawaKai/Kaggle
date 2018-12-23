import pandas as pd

tour = pd.read_csv("./data/tour_distances1_1.csv", sep=",")

start0 = tour.iloc[0, 0]
start1 = tour.iloc[0, 1]

end_column = list(tour.iloc[1:, 1])
print(end_column)
path = [start0, start1] + end_column

dict_ = {"Path": path}

pd.DataFrame.from_dict(dict_).to_csv("./submission_concorde1_en.csv", sep=",", index=False)