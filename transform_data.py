import glob
import os

import pandas as pd

path = "data/raw/"
all_sensors_data = []
for i in range(1, 4):
    csv_files = glob.glob(os.path.join(path, f"*_sensor{i}.csv"))
    sensor_data = pd.concat(map(pd.read_csv, csv_files))
    sensor_data["sensor_id"] = i
    all_sensors_data.append(sensor_data)
df = pd.concat(all_sensors_data)
df["date"] = pd.to_datetime(dict(year=df.year, month=df.month, day=df.day))
print(df)

df_day = (
    df.groupby(by=["store_location", "sensor_id", "date"])["visit_count"]
    .sum()
    .reset_index()
)

df_day.dropna(inplace=True)
df_day.query("visit_count > 0", inplace=True)
df_day["day_of_week"] = df_day["date"].dt.dayofweek

df_day["moving_avg_4"] = (
    df_day.groupby(by=["day_of_week", "sensor_id"])["visit_count"]
    .rolling(window=4, min_periods=1)
    .mean()
    .reset_index(level=[0, 1], drop=True)
)

df_day = df_day[
    [
        "store_location",
        "sensor_id",
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
