from datetime import date

import numpy as np

from src.sensor import (VisitSensor)


class StoreSensor:
    def __init__(
        self,
        location: str,
        avg_visit: int,
        std_visit: int,
        perc_malfunction: float = 0,
        perc_break: float = 0,
    ) -> None:
        """Initialize a store"""
        self.name = location
        self.sensors = dict()

        # To always get the same result when asking for the same store
        seed = np.sum(list(self.name.encode("ascii")))
        np.random.seed(seed=seed)

        # 80/20: most people take the main entrance
        traffic_percentage = [0.58, 0.30, 0.07, 0.05]
        np.random.shuffle(traffic_percentage)

        # Initialization of the store's sensors
        # To keep things simple, we assume each store has eight sensors
        # Otherwise we would need to dynamically create traffic_percentages that sum to 1
        sensor_labels = ['A', 'B', 'C', 'D']
        for i, label in enumerate(sensor_labels):
            sensor = VisitSensor(
                traffic_percentage[i] * avg_visit,
                traffic_percentage[i] * std_visit,
                perc_malfunction,
                perc_break,
            )
            self.sensors[label] = sensor

    def get_sensor_traffic(self, sensor_id: str, business_date: date) -> int:
        """Return the traffic for one sensor at a date"""
        return self.sensors[sensor_id].get_visit_count(business_date)

    def get_all_traffic(self, business_date: date) -> int:
        """Return the traffic for all store sensors at a date"""
        return sum([self.sensors[i].get_visit_count(business_date) for i in ["A", "B", "C", "D"]])
