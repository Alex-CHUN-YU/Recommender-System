import numpy as np

# 利用 numpy 判斷 array 是不是皆為 0
vector = np.zeros(750)
one = np.ones(0)
vector = np.append(vector, one)
print(np.reshape(vector, (5, 150)))
if np.max(vector, 0) == 0.0 and np.min(vector, 0) == 0:
	print("zero element")
print(np.max(vector))
print(np.min(vector))
