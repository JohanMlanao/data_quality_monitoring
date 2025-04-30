import numpy as np
import random
from datetime import date

class Sensor:

    def __init__(self, avg_visit: int, std_visit: int) -> None:
        self.avg_visit = avg_visit
        self.std_visit = std_visit

    def simulate_visit(self, business_date: date, hour: int) -> int:
        """Simulate the number of person detected by the sensor
        during the day"""

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
        if hour < 8 or hour > 19:
            visit = -1
        else:
            visit /= 11

        return np.floor(visit)


if __name__ == "__main__":
    capteur = Sensor(1500, 150)
    print(capteur.simulate_visit(date(year=2023, month=10, day=25), hour=8))
