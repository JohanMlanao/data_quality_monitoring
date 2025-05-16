import glob
import os

import pandas as pd


def load_sensor_data(path: str = "data/raw/") -> pd.DataFrame:
    """
    Loads and combines CSV files for multiple sensors into a single DataFrame.
    """
    sensors = ["A", "B", "C", "D"]
    all_sensors_data = []

    for i in sensors:
        csv_files = glob.glob(os.path.join(path, f"*_sensor{i}.csv"))
        if not csv_files:
            continue
        sensor_data = pd.concat(map(pd.read_csv, csv_files))
        sensor_data["sensor_id"] = i
        all_sensors_data.append(sensor_data)

    return (
        pd.concat(all_sensors_data, ignore_index=True)
        if all_sensors_data
        else pd.DataFrame()
    )


def prepare_date_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a 'date' column by combining 'year', 'month', and 'day' columns.
    """
    if df.empty:
        return df
    df["date"] = pd.to_datetime(dict(year=df.year, month=df.month, day=df.day))
    return df


def aggregate_daily_visits(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates total visits by store, sensor, and date.
    Drops rows with nulls or zero visits and adds day-of-week info.
    """
    if df.empty:
        return df

    df_day = (
        df.groupby(by=["store_location", "sensor_id", "date"])["visit_count"]
        .sum()
        .reset_index()
    )
    df_day.dropna(inplace=True)
    df_day = df_day.query("visit_count > 0")

    if df_day.empty:
        return df_day

    df_day["day_of_week"] = df_day["date"].dt.dayofweek
    return df_day


def add_moving_average_and_change(df_day: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a 4-period rolling average and percent change vs the moving average.
    """
    if df_day.empty:
        return df_day
    df_day["moving_avg_4"] = (
        df_day.groupby(by=["day_of_week", "sensor_id"])["visit_count"]
        .rolling(window=4, min_periods=1)
        .mean()
        .reset_index(level=[0, 1], drop=True)
    )

    df_day["pct_change"] = df_day.apply(
        lambda x: (
            abs(x["visit_count"] - x["moving_avg_4"]) / x["moving_avg_4"]
            if x["moving_avg_4"] != 0
            else 0
        ),
        axis=1,
    )
    return df_day[
        [
            "store_location",
            "sensor_id",
            "date",
            "day_of_week",
            "visit_count",
            "moving_avg_4",
            "pct_change",
        ]
    ]


def main():
    df = load_sensor_data()
    if not df.empty:
        df = prepare_date_column(df)
        df_day = aggregate_daily_visits(df)
        df_day = add_moving_average_and_change(df_day)
        print(df_day.sort_values(by="date"))
        df_day.to_parquet(
            path="/data/processed/data.parquet", index=False
        )
    else:
        print("Input DataFrame is empty — skipping processing.")


if __name__ == "__main__":
    main()
