import numpy as np

dict_ = {"horse": lambda: max(0, np.random.normal(5, 2, 1)[0]),
         "ball": lambda: max(0, 1 + np.random.normal(1, 0.3, 1)[0]),
         "bike": lambda: max(0, np.random.normal(20, 10, 1)[0]),
         "train": lambda: max(0, np.random.normal(10, 5, 1)[0]),
         "coal": lambda: 47 * np.random.beta(0.5, 0.5, 1)[0],
         "book": lambda: np.random.chisquare(2, 1)[0],
         "doll": lambda: np.random.gamma(5, 1, 1)[0],
         "block": lambda: np.random.triangular(5, 10, 20, 1)[0],
         "gloves": lambda: 3.0 + np.random.rand(1)[0] if np.random.rand(1) < 0.3 else np.random.rand(1)[0]}

