from src.sensor import VisitSensor
import unittest
from datetime import date


class TestVisitSensor(unittest.TestCase):

    def test_monday_open(self):
        visit_sensor = VisitSensor(avg_visit=1200, std_visit=300)
        visit_count = visit_sensor.simulate_visit_count(
            date(year=2025, month=4, day=7), business_hour=12
        )

        self.assertFalse(visit_count == -1)

    def test_monday_closed(self):
        visit_sensor = VisitSensor(avg_visit=1200, std_visit=300)
        visit_count = visit_sensor.simulate_visit_count(
            date(year=2025, month=4, day=7), business_hour=22
        )

        self.assertFalse(visit_count != -1)

    def test_tuesday_open(self):
        visit_sensor = VisitSensor(avg_visit=1200, std_visit=300)
        visit_count = visit_sensor.simulate_visit_count(
            date(year=2025, month=4, day=8), business_hour=12
        )

        self.assertFalse(visit_count == -1)

    def test_tuesday_closed(self):
        visit_sensor = VisitSensor(avg_visit=1200, std_visit=300)
        visit_count = visit_sensor.simulate_visit_count(
            date(year=2025, month=4, day=12), business_hour=22
        )

        self.assertFalse(visit_count != -1)

    def test_wednesday_open(self):
        visit_sensor = VisitSensor(avg_visit=1200, std_visit=300)
        visit_count = visit_sensor.simulate_visit_count(
            date(year=2025, month=4, day=9), business_hour=12
        )

        self.assertFalse(visit_count == -1)

    def test_wednesday_closed(self):
        visit_sensor = VisitSensor(avg_visit=1200, std_visit=300)
        visit_count = visit_sensor.simulate_visit_count(
            date(year=2025, month=4, day=12), business_hour=22
        )

        self.assertFalse(visit_count != -1)

    def test_thursday_open(self):
        visit_sensor = VisitSensor(avg_visit=1200, std_visit=300)
        visit_count = visit_sensor.simulate_visit_count(
            date(year=2025, month=4, day=10), business_hour=12
        )

        self.assertFalse(visit_count == -1)

    def test_thursday_closed(self):
        visit_sensor = VisitSensor(avg_visit=1200, std_visit=300)
        visit_count = visit_sensor.simulate_visit_count(
            date(year=2025, month=4, day=12), business_hour=22
        )

        self.assertFalse(visit_count != -1)

    def test_friday_open(self):
        visit_sensor = VisitSensor(avg_visit=1200, std_visit=300)
        visit_count = visit_sensor.simulate_visit_count(
            date(year=2025, month=4, day=11), business_hour=12
        )

        self.assertFalse(visit_count == -1)

    def test_friday_closed(self):
        visit_sensor = VisitSensor(avg_visit=1200, std_visit=300)
        visit_count = visit_sensor.simulate_visit_count(
            date(year=2025, month=4, day=12), business_hour=22
        )

        self.assertFalse(visit_count != -1)

    def test_saturday_open(self):
        visit_sensor = VisitSensor(avg_visit=1200, std_visit=300)
        visit_count = visit_sensor.simulate_visit_count(
            date(year=2025, month=4, day=12), business_hour=12
        )

        self.assertFalse(visit_count == -1)

    def test_saturday_closed(self):
        visit_sensor = VisitSensor(avg_visit=1200, std_visit=300)
        visit_count = visit_sensor.simulate_visit_count(
            date(year=2025, month=4, day=12), business_hour=22
        )

        self.assertFalse(visit_count != -1)

    def test_sunday_closed(self):
        visit_sensor = VisitSensor(avg_visit=1200, std_visit=300)
        visit_count = visit_sensor.simulate_visit_count(
            date(year=2025, month=4, day=12), business_hour=22
        )

        self.assertFalse(visit_count != -1)

    def test_with_break(self):
        visit_sensor = VisitSensor(avg_visit=1200, std_visit=300, perc_break=10)
        visit_count = visit_sensor.get_visit_count(
            date(year=2025, month=4, day=12), business_hour=12
        )

        self.assertEqual(visit_count, 0)

    def test_with_malfunction(self):
        visit_sensor = VisitSensor(avg_visit=1200, std_visit=300, perc_malfunction=123)
        visit_count = visit_sensor.get_visit_count(
            date(year=2025, month=4, day=12), business_hour=12
        )

        self.assertEqual(visit_count, 19.0)

    def test_without_malfunction(self):
        visit_sensor = VisitSensor(avg_visit=1200, std_visit=300, perc_malfunction=0)
        visit_count = visit_sensor.get_visit_count(
            date(year=2025, month=4, day=12), business_hour=12
        )

        self.assertEqual(visit_count, 96)


if __name__ == "__main__":
    unittest.main()
