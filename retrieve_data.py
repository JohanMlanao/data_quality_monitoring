import sys
from datetime import date, timedelta

import pandas as pd
import requests


def get_data(
    business_name: str,
    business_year: int,
    business_month: int,
    business_day: int,
    business_hour: int,
) -> int:
    r = requests.get(
        "https://data-quality-monitoring-j9nq.onrender.com",
        params=f"store_name={business_name}&year={business_year}&month={business_month}&day={business_day}&hour={business_hour}",
    )
    return r.text


if __name__ == "__main__":
    if len(sys.argv) > 1:
        store_name, hour, day, month, year = [v for v in sys.argv[1].split("-")]
    else:
        store_name, hour, day, month, year = ["Bordeaux", 10, 1, 5, 2025]

    init_date = date(year=int(year), month=int(month), day=int(day))
    init_hour = int(hour)
    data = []
    while init_date < date.today():
        init_hour += 1
        if init_hour == 24:
            init_date += timedelta(days=1)
            init_hour = 0
        visit_count = get_data(
            business_name=store_name,
            business_year=init_date.year,
            business_month=init_date.month,
            business_day=init_date.day,
            business_hour=int(init_hour),
        )
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

    # Example: print first 2 rows of each group
    for (year, month), group_df in grouped.items():
        filename = f"data/raw/data_{year}_{month:02}.csv"
        group_df.to_csv(filename, index=False)
