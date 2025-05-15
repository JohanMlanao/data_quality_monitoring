import unittest
from datetime import date

from src.store import StoreSensor


class TestStoreSensor(unittest.TestCase):

    def test_get_sensor_traffic(self):
        store = StoreSensor(location="Lille", avg_visit=1500, std_visit=300)
        traffic = store.get_sensor_traffic(
            sensor_id=1, business_date=date(year=2025, month=4, day=2)
        )
        self.assertEqual(traffic, 10)

    def test_get_all_traffic(self):
        store = StoreSensor(location="Lille", avg_visit=1500, std_visit=300)
        traffic = store.get_all_traffic(business_date=date(year=2025, month=4, day=2))
        self.assertEqual(traffic, 149)

    def test_store_closed_sunday(self):
        store = StoreSensor(location="Lille", avg_visit=1500, std_visit=300)
        traffic = store.get_all_traffic(business_date=date(year=2025, month=5, day=4))
        self.assertEqual(traffic, 0)


if __name__ == "__main__":
    unittest.main()
