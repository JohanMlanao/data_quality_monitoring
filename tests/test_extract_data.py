import unittest
from datetime import date, timedelta
from unittest.mock import MagicMock, patch

from extract_data import collect_traffic_data, get_data


class TestExtractData(unittest.TestCase):
    @patch("extract_data.requests.get")  # Mock 'requests.get'
    def test_get_data_success(self, mock_get):
        # Mock a successful HTTP response
        mock_response = MagicMock()
        mock_response.text = "42"  # Simulated visit_count
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        text, status = get_data("store_location=test")
        self.assertEqual(text, "42")
        self.assertEqual(status, 200)

    @patch("extract_data.get_data")
    def test_collect_traffic_data_previous_month(self, mock_get_data):
        # Always return 7 as dummy visit count
        mock_get_data.return_value = ("7", 200)

        # Use fixed "today" for deterministic previous month calculations
        today = date(2025, 5, 15)
        start_date = today  # It's only used to compute the previous month

        store_locations = ["TestStore"]
        sensors = [0]

        # Patch `date.today()` in the extract_data module
        with patch("extract_data.date") as mock_date:
            mock_date.today.return_value = today
            mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

            data = collect_traffic_data(store_locations, sensors, start_date)

        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

        sample = data[0]
        self.assertIn("store_location", sample)
        self.assertIn("sensor_id", sample)
        self.assertIn("visit_count", sample)
        self.assertIn("hour", sample)

        # Ensure all data is from the previous month
        for row in data:
            self.assertEqual(row["month"], 4)  # April
            self.assertEqual(row["year"], 2025)

    @patch("extract_data.get_data")
    def test_collect_data_outside_business_hours(self, mock_get_data):
        # Return value won't be used for non-business hours
        mock_get_data.return_value = ("999", 200)

        today = date(2025, 5, 15)
        start_date = today
        store_locations = ["TestStore"]
        sensors = [1]

        with patch("extract_data.date") as mock_date:
            mock_date.today.return_value = today
            mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

            data = collect_traffic_data(store_locations, sensors, start_date)

        # Filter for non-business hours
        non_business_hours = [
            row for row in data if row["hour"] < 8 or row["hour"] > 19
        ]
        self.assertTrue(all(row["visit_count"] == 0 for row in non_business_hours))

    @patch("extract_data.get_data")
    def test_collect_data_business_hours_calls_get_data(self, mock_get_data):
        mock_get_data.return_value = ("3", 200)

        today = date(2025, 5, 15)
        start_date = today
        store_locations = ["A"]
        sensors = [1]

        with patch("extract_data.date") as mock_date:
            mock_date.today.return_value = today
            mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

            collect_traffic_data(store_locations, sensors, start_date)

        # Assert get_data was called exactly for each business-hour slot in the month
        expected_days = 30  # April has 30 days
        expected_hours = 12  # From 8 to 19 inclusive
        expected_calls = (
            expected_days * expected_hours * len(store_locations) * len(sensors)
        )

        self.assertEqual(mock_get_data.call_count, expected_calls)


if __name__ == "__main__":
    unittest.main()
