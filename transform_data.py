import glob
import os

import pandas as pd

path = "data/raw/"
csv_files = glob.glob(os.path.join(path, "*.csv"))
df = pd.concat(map(pd.read_csv, csv_files))
print(df)

df_day = (
    df.groupby(by=["store_location", "year", "month", "day"])["visit_count"]
    .sum()
    .reset_index()
)

print(df_day)

df_day.dropna(inplace=True)

regular_values = (df_day['visit_count'] > 0)

print(df_day[regular_values])
