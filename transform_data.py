import glob
import os

import pandas as pd

path = "data/raw/"
csv_files = glob.glob(os.path.join(path, "*.csv"))
df = pd.concat(map(pd.read_csv, csv_files))
print(df)
