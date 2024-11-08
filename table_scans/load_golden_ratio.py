import pandas as pd
import numpy as np

file = "golden_ratio_360degrees_500projections.csv"

df = pd.read_csv(file)

list_angles = np.array(df['angles'])
print(list_angles)