import glob
import os

import pandas as pd

path = "data/raw/"
csv_files = glob.glob(os.path.join(path, "*.csv"))
df = pd.concat(map(pd.read_csv, csv_files))
df["date"] = pd.to_datetime(dict(year=df.year, month=df.month, day=df.day))
print(df)

df_day = df.groupby(by=["store_location", "date"])["visit_count"].sum().reset_index()

df_day.dropna(inplace=True)
df_day.query("visit_count > 0", inplace=True)
df_day["day_of_week"] = df_day["date"].dt.dayofweek

df_day["moving_avg_4"] = (
    df_day.groupby(by=["day_of_week"])["visit_count"]
    .rolling(window=4, min_periods=1)
    .mean()
    .reset_index(level=0, drop=True)
)
df_day = df_day[
    [
        "store_location",
        "date",
        "day_of_week",
        "visit_count",
        "moving_avg_4",
    ]
]

df_day["pct_change"] = df_day.apply(
    lambda x: (abs(x["visit_count"] - x["moving_avg_4"])) / x["moving_avg_4"], axis=1
)
print(df_day.sort_values(by="date"))

df_day.to_parquet(path="data/processed/data.parquet", index=False)
