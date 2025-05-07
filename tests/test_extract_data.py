import unittest
from datetime import date
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
    def test_collect_traffic_data_valid(self, mock_get_data):
        # Simulate a successful API response with visit_count = 5 and status code 200
        mock_get_data.return_value = ("5", 200)

        start_date = date.today().replace(
            day=1
        )  # Use 1st of the current month as start date
        store_location = "TestStore"

        # Patch the 'date.today()' call inside collect_traffic_data to control the end date
        with patch("extract_data.date") as mock_date:
            mock_date.today.return_value = start_date.replace(
                day=2
            )  # Simulate today as 2nd
            mock_date.side_effect = lambda *args, **kw: date(
                *args, **kw
            )  # Let date(...) still work normally

            # Call the function under test
            data = collect_traffic_data(store_location, start_date)

        # Check that data is returned as a list of dictionaries
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)  # Ensure we have at least one record
        self.assertIn("store_location", data[0])  # Ensure required keys are present
        self.assertIn("visit_count", data[0])

    @patch(
        "extract_data.get_data"
    )  # Mock the 'get_data' function to simulate a failed response
    def test_collect_traffic_data_404(self, mock_get_data):
        # Simulate API returning 404 Not Found for the given store
        mock_get_data.return_value = ("Not Found", 404)

        start_date = date.today().replace(
            day=1
        )  # Use 1st of the current month as start date
        store_location = "InvalidStore"

        # Patch 'date.today()' to simulate a short date range
        with patch("extract_data.date") as mock_date:
            mock_date.today.return_value = start_date.replace(
                day=2
            )  # Simulate today as 2nd
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

            # Call the function — it should exit early due to 404 and return an empty list
            data = collect_traffic_data(store_location, start_date)

        self.assertEqual(
            data, []
        )  # Assert that no data was collected due to invalid store


if __name__ == "__main__":
    unittest.main()
