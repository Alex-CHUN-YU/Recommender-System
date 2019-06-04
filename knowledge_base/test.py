import numpy as np
# two different array element sum test
thresholds = [0.8, 0.825, 0.85, 0.875, 0.9, 0.925, 0.95, 0.975]
scores = [0.7666666666666667, 0.7333333333333333, 0.7333333333333333, 0.6833333333333333, 0.6333333333333333, 0.4666666666666667, 0.13333333333333333, 0.08333333333333333]
print("two different array element sum:", end = "")
print(np.sum([scores,thresholds], axis = 0))
print("max element:", end = "")
print(np.max(np.sum([scores,thresholds], axis = 0)))