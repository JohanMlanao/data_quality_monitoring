import math
from datetime import date, timedelta

import numpy as np


class VisitSensor:

    def __init__(
        self,
        store_name: str,
        avg_visit: int,
        std_visit: int,
        perc_break: float = 0.015,
        perc_malfunction: float = 0.035,
    ) -> None:
        self.store_name = store_name
        self.avg_visit = avg_visit
        self.std_visit = std_visit
        self.perc_break = perc_break
        self.perc_malfunction = perc_malfunction

    def simulate_visit_count(self, business_date: date) -> int:

        # Ensure reproducibility of measurements
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

        # Return an integer
        return math.floor(visit/11)

    def get_visit_count(self, business_date: date) -> int:
        np.random.seed(seed=business_date.toordinal())
        proba_malfunction = np.random.random()

        # The sensor can break sometimes
        if proba_malfunction < self.perc_break:
            print("break")
            return 0

        visit = self.simulate_visit_count(business_date)

        # The sensor can also malfunction
        if proba_malfunction < self.perc_malfunction:
            print("malfunction")
            visit = np.floor(visit * 0.2)
        return visit
