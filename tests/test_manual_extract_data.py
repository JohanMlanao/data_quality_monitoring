import unittest
from datetime import date
from unittest.mock import MagicMock, patch

from etl.manual_extract_data import (collect_traffic_data, get_data,
                                     is_valid_sensor, save_data_by_month)


class TestTrafficDataScript(unittest.TestCase):

    @patch("manual_extract.requests.get")
    def test_get_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "100"
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        text, status = get_data("store_location=Test")
        self.assertEqual(text, "100")
        self.assertEqual(status, 200)

    def test_is_valid_sensor(self):
        self.assertTrue(is_valid_sensor("A"))
        self.assertTrue(is_valid_sensor("D"))
        self.assertFalse(is_valid_sensor("4"))
        self.assertFalse(is_valid_sensor("abc"))
        self.assertFalse(is_valid_sensor(""))

    @patch("manual_extract.get_data")
    @patch("manual_extract.date")
    def test_collect_traffic_data_with_valid_sensor(self, mock_date, mock_get_data):
        mock_get_data.return_value = ("42", 200)

        # Simulate today = 2025-05-15 and start date = same day
        mock_date.today.return_value = date(2025, 5, 15)
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

        data = collect_traffic_data("TestStore", "2", date(2025, 5, 15))

        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 24)
        for row in data:
            self.assertIn("visit_count", row)
            self.assertIn("hour", row)

    @patch("manual_extract.get_data")
    @patch("manual_extract.date")
    def test_collect_traffic_data_with_invalid_store(self, mock_date, mock_get_data):
        # Simulate the 404 response
        mock_get_data.return_value = ("0", 404)

        mock_date.today.return_value = date(2025, 5, 15)
        mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

        data = collect_traffic_data("BadStore", "", date(2025, 5, 15))
        self.assertEqual(data, [])

    @patch("manual_extract.pd.DataFrame.to_csv")
    def test_save_data_by_month_with_invalid_sensor(self, mock_to_csv):
        data = [
            {
                "store_location": "TestStore",
                "visit_count": 5,
                "hour": 10,
                "day": 15,
                "month": 5,
                "year": 2025,
            }
        ]

        save_data_by_month(data, "TestStore", "")  # Invalid sensor

        mock_to_csv.assert_called_once()
        args, kwargs = mock_to_csv.call_args
        self.assertIn("data/raw/data_TestStore_2025_05.csv", args[0])


if __name__ == "__main__":
    unittest.main()
