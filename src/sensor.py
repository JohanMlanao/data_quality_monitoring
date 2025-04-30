import random
import sys
from datetime import date, timedelta

import numpy as np


class VisitSensor:

    def __init__(
        self,
        avg_visit: int,
        std_visit: int,
        perc_break: float = 0.015,
        perc_malfunction: float = 0.035,
    ) -> None:
        self.avg_visit = avg_visit
        self.std_visit = std_visit
        self.perc_break = perc_break
        self.perc_malfunction = perc_malfunction


    def simulate_visit_count(self, business_date: date, business_hour: int) -> int:

        # Ensure reproducibilty of measurements
        np.random.seed(seed=business_date.toordinal())

        # Find out which day the business_date corresponds to: Monday = 0, Sunday = 6
        week_day = business_date.weekday()

        visit = np.random.normal(self.avg_visit, self.std_visit)
        # More traffic on Wednesdays (2), Fridays (4) and Saturdays (5)
        if week_day == 2:
            visit *= 1.10
        if week_day == 4:
            visit *= 1.25
        if week_day == 5:
            visit *= 1.35

        # No traffic on Sundays(6)
        if week_day == 6:
            visit = -1

        # Same traffic between 8am and 7pm and no traffic between 8pm and 7am
        if business_hour < 8 or business_hour > 19:
            visit = -1
        else:
            visit /= 11

        # Return an integer
        return np.floor(visit)

    def get_visit_count(self, business_date: date, business_hour: int) -> int:
        np.random.seed(seed=business_date.toordinal())
        proba_malfunction = np.random.random()

        # The sensor can break sometimes
        if proba_malfunction < self.perc_break:
            print("break")
            return 0

        visit = self.simulate_visit_count(business_date, business_hour)

        # The sensor can also malfunction
        if proba_malfunction < self.perc_malfunction:
            print("malfunction")
            visit = np.floor(visit * 0.2)
        return visit



if __name__ == "__main__":
    if len(sys.argv) > 1:
        year, month, day, hour = [int(v) for v in sys.argv[1].split("-")]
    else:
        year, month, day, hour = [2025, 5, 24, 10]
    queried_date = date(year, month, day)

    capteur = VisitSensor(1500, 150)
    init_date = date(year=2022, month=1, day=1)
    init_hour = 1
    while init_date < date(year=2024, month=1, day=1):
        init_hour += 1
        if init_hour == 24:
            init_date += timedelta(days=1)
            init_hour = 0
        visit_count = capteur.get_visit_count(init_date, init_hour)
        print(init_date, init_hour, visit_count)

