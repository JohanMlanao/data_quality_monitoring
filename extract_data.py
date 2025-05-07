from datetime import date, datetime, timedelta

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


def get_user_inputs() -> tuple[str, date, str]:
    """Prompts the user for store location, date, and sensor ID input."""
    store_location = input("Please enter the store location: ")
    date_input = input("Please enter a date in the format DD-MM-YYYY: ")
    business_date = datetime.strptime(date_input, "%d-%m-%Y").date()
    sensor_id = input(
        "To view sensor traffic, enter a number from 1 to 8, or press Enter to view all traffic: "
    )
    return store_location, business_date, sensor_id


def is_valid_sensor(sensor_id: str) -> bool:
    """Checks whether the sensor_id is a valid number from 1 to 7."""
    return sensor_id.isdigit() and 0 < int(sensor_id) < 8


def collect_traffic_data(store_location: str, start_date: date) -> list[dict]:
    """
    Iterates from start_date to today, hour by hour, collecting traffic data.
    Returns a list of data rows.
    """
    data = []
    current_date = start_date
    current_hour = 0

    while current_date < date.today():
        current_hour += 1

        if current_hour == 24:
            current_date += timedelta(days=1)
            current_hour = 0

        if current_hour < 8 or current_hour > 19:
            visit_count = 0
        else:
            params = (
                f"store_location={store_location}"
                f"&year={current_date.year}&month={current_date.month}&day={current_date.day}"
            )
            visit_count, status = get_data(business_parameter=params)

            if status == 404:
                print("\nThe specified store location could not be found.")
                return []

        row = {
            "store_location": store_location,
            "visit_count": visit_count,
            "hour": current_hour,
            "day": current_date.day,
            "month": current_date.month,
            "year": current_date.year,
        }
        data.append(row)

    return data


def save_data_by_month(data: list[dict], store_location: str, sensor_id: str):
    """Groups data by month and saves each group as a separate CSV file."""
    df = pd.DataFrame(data)
    grouped = dict(tuple(df.groupby(["year", "month"])))

    for (year, month), group_df in grouped.items():
        if is_valid_sensor(sensor_id):
            filename = f"data/raw/data_{store_location}_{year}_{month:02}_sensor{sensor_id}.csv"
        else:
            filename = f"data/raw/data_{store_location}_{year}_{month:02}.csv"

        group_df.to_csv(filename, index=False)


def main():
    store_location, business_date, sensor_id = get_user_inputs()

    if sensor_id and not is_valid_sensor(sensor_id):
        print("Sensor ID not selected or is invalid; returning all traffic by default.")

    data = collect_traffic_data(store_location, business_date)

    if data:
        save_data_by_month(data, store_location, sensor_id)


if __name__ == "__main__":
    main()
