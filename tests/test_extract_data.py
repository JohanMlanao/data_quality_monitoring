import unittest
from datetime import date, timedelta
from unittest.mock import MagicMock, patch

from extract_data import collect_traffic_data, get_data, is_valid_sensor


class TestExtractData(unittest.TestCase):

    def test_is_valid_sensor(self):
        self.assertTrue(is_valid_sensor("1"))
        self.assertTrue(is_valid_sensor("7"))
        self.assertFalse(is_valid_sensor("0"))
        self.assertFalse(is_valid_sensor("8"))
        self.assertFalse(is_valid_sensor("abc"))
        self.assertFalse(is_valid_sensor(""))

    @patch("extract_data.requests.get")  # Mock 'requests.get' in your module
    def test_get_data_success(self, mock_get):
        # Create a mock response object to simulate a successful API call
        mock_response = MagicMock()
        mock_response.text = "some text"  # Simulate response body
        mock_response.status_code = 200  # Simulate HTTP 200 OK

        # Set the mock to return the mock response when called
        mock_get.return_value = mock_response

        # Call the actual function with a test parameter
        text, status = get_data("store_location=test")

        # Verify the function correctly returns the mocked response values
        self.assertEqual(text, "some text")  # Check if response text is as expected
        self.assertEqual(status, 200)  # Check if status code is as expected

    @patch(
        "extract_data.get_data"
    )  # Mock the 'get_data' function in 'extract_data' module
    def test_collect_traffic_data_all_sensors_today(self, mock_get_data):
        # Mock get_data to return consistent values
        mock_get_data.return_value = (5, 200)

        store_location = "TestStore"
        today = date(2025, 5, 14)  # fixed date for deterministic test
        start_date = today  # same as today

        # Patch date.today inside the collect_traffic_data module
        with patch("extract_data.date") as mock_date:
            mock_date.today.return_value = today
            mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)

            data = collect_traffic_data(store_location, "all_sensors", start_date)

        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn("store_location", data[0])
        self.assertIn("sensor_id", data[0])
        self.assertIn("visit_count", data[0])
        self.assertIn("hour", data[0])

    @patch("extract_data.get_data")
    @patch("extract_data.is_valid_sensor")
    def test_store_location_not_found(self, mock_is_valid_sensor, mock_get_data):
        # Set up mocks
        mock_is_valid_sensor.return_value = False
        mock_get_data.return_value = (0, 404)

        # Set start_date to a recent date to limit iteration
        start_date = date.today() - timedelta(days=1)

        result = collect_traffic_data(
            store_location="invalid_store",
            sensor_id="dummy_sensor",
            start_date=start_date,
        )

        self.assertEqual(
            result, [], "Should return empty list when store location is invalid."
        )


if __name__ == "__main__":
    unittest.main()
