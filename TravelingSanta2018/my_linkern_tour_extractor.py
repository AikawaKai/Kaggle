import pandas as pd

file_ = pd.read_csv("./data/linkern2.tour", sep=" ", header=None)
print(file_)
trip = list(file_.iloc[:, 0]) + [0]
print(trip[0:10])
print(trip[-10:])

dict_ = {"Path": trip}

pd.DataFrame.from_dict(dict_).to_csv("./neon_submission.csv", sep=",", index=False)