from datetime import date, datetime, timedelta
from itertools import product

import pandas as pd
import requests


def get_data(business_parameter: str) -> tuple[str, int]:
    """
    Sends a GET request to the data quality monitoring API with the given business parameter.
    Returns the response text and status code.
    """
    r = requests.get(
        "https://data-quality-monitoring-j9nq.onrender.com",
        params=business_parameter,
    )
    return r.text, r.status_code


def get_input() -> tuple[list[str], date, list[int]]:
    store_locations = ["Lille", "Paris", "Lyon", "Bordeaux", "Marseille"]
    sensors = [0, 1, 2, 3]
    business_date = date.today()
    return store_locations, business_date, sensors


def collect_traffic_data(
    store_locations: list[str], sensors: list[int], start_date: date
) -> list[dict]:
    """
    Iterates from start_date to today, hour by hour, collecting traffic data.
    Returns a list of data rows.
    """
    data = []
    current_hour = 0
    # Replace the day with 1 to get the first day of the month
    first_day = start_date.replace(day=1)
    last_day_previous_month = first_day - timedelta(days=1)
    # Retrieve the first day of the previous month
    current_date = last_day_previous_month.replace(day=1)
    condition = current_date <= last_day_previous_month
    while current_date <= last_day_previous_month:
        current_hour += 1
        if current_hour == 24:
            current_date += timedelta(days=1)
            current_hour = 0
        if current_date > last_day_previous_month:
            break

        if current_hour < 8 or current_hour > 19:
            for store_location, sensor in product(store_locations, sensors):
                sensor_row = {
                    "store_location": store_location,
                    "sensor_id": sensor,
                    "visit_count": 0,
                    "hour": current_hour,
                    "day": current_date.day,
                    "month": current_date.month,
                    "year": current_date.year,
                }
                data.append(sensor_row)
        else:
            for store_location, sensor in product(store_locations, sensors):
                params = (
                    f"store_location={store_location}"
                    f"&year={current_date.year}&month={current_date.month}&day={current_date.day}&sensor_id={sensor}"
                )
                visit_count, status = get_data(business_parameter=params)
                sensor_row = {
                    "store_location": store_location,
                    "sensor_id": sensor,
                    "visit_count": visit_count,
                    "hour": current_hour,
                    "day": current_date.day,
                    "month": current_date.month,
                    "year": current_date.year,
                }
                data.append(sensor_row)
    return data


def save_data_by_month(data: list[dict]):
    """Groups data by month and saves each group as a separate CSV file."""
    df = pd.DataFrame(data)
    grouped = dict(tuple(df.groupby(["year", "month"])))

    for (year, month), group_df in grouped.items():
        filename = f"~/data_quality_monitoring/data/raw/data_{year}_{month:02}.csv"
        group_df.to_csv(filename, index=False)


def main():
    store_location, business_date, sensor_id = get_input()

    data = collect_traffic_data(store_location, sensor_id, business_date)

    if data:
        save_data_by_month(data)


if __name__ == "__main__":
    main()
