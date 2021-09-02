import numpy as np
import pandas as pd

data = pd.read_csv("data/summer.csv", index_col=0)
df = pd.DataFrame(data=data, dtype=np.datetime64)
print(data.dtypes)