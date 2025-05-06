from datetime import date, datetime, timedelta

import pandas as pd
import requests


def get_data(
    business_parameter: str,
) -> int:
    r = requests.get(
        "https://data-quality-monitoring-j9nq.onrender.com",
        params=business_parameter,
    )
    return r.text


if __name__ == "__main__":
    store_name = input("Please enter the store location: ")
    date_input = input("Please enter a date in the format DD-MM-YYYY: ")
    date_format = "%d-%m-%Y"
    business_date = datetime.strptime(date_input, date_format).date()
    sensor_id = input(
        "To view sensor traffic, enter a number from 1 to 8, or press Enter to view all traffic: "
    )
    init_date = business_date
    if sensor_id and (0 < int(sensor_id) < 8):
        sensor_id = int(sensor_id)
        parameter = f"store_name={store_name}&year={init_date.year}&month={init_date.month}&day={init_date.day}&sensor_id={sensor_id}"
    else:
        print("Sensor ID not selected or is invalid; returning all traffic by default.")
        parameter = f"store_name={store_name}&year={init_date.year}&month={init_date.month}&day={init_date.day}"
    init_hour = 0
    data = []
    while init_date < date.today():
        init_hour += 1
        if init_hour == 24:
            init_date += timedelta(days=1)
            init_hour = 0
        if init_hour < 8 or init_hour > 19:
            visit_count = -1
        else:
            visit_count = get_data(business_parameter=parameter)
        row = {
            "store_name": store_name,
            "visit_count": visit_count,
            "hour": init_hour,
            "day": init_date.day,
            "month": init_date.month,
            "year": init_date.year,
        }
        data.append(row)
    df = pd.DataFrame(data)
    grouped = dict(tuple(df.groupby(["year", "month"])))

    for (year, month), group_df in grouped.items():
        # filename = f"data/raw/data_{store_name}_{year}_{month:02}.csv"
        if sensor_id and (sensor_id < 8 and sensor_id > 0):
            filename = (
                f"data/raw/data_{store_name}_{year}_{month:02}_sensor{sensor_id}.csv"
            )
        else:
            filename = f"data/raw/data_{store_name}_{year}_{month:02}.csv"
        group_df.to_csv(filename, index=False)
