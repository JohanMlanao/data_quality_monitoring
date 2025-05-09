import unittest
import pandas as pd
from unittest.mock import patch
from transform_data import (
    load_sensor_data,
    prepare_date_column,
    aggregate_daily_visits,
    add_moving_average_and_change
)


class TestTransformData(unittest.TestCase):

    @patch("glob.glob")
    @patch("pandas.concat")
    @patch("pandas.read_csv")
    def test_load_sensor_data(self, mock_read_csv, mock_concat, mock_glob):
        # Mocking glob to simulate the presence of CSV files
        mock_glob.return_value = ["file1.csv", "file2.csv"]

        # Mock the behavior of pd.read_csv to return a simple DataFrame
        mock_read_csv.return_value = pd.DataFrame({
            "store_location": ["A", "B"],
            "sensor_id": [1, 1],
            "year": [2023, 2023],
            "month": [5, 5],
            "day": [1, 2],
            "visit_count": [100, 200]
        })

        # Mock pandas concat
        mock_concat.return_value = pd.DataFrame({
            "store_location": ["A", "B"],
            "sensor_id": [1, 1],
            "year": [2023, 2023],
            "month": [5, 5],
            "day": [1, 2],
            "visit_count": [100, 200]
        })

        # Test
        df = load_sensor_data(path="data/raw/")
        self.assertFalse(df.empty)
        self.assertIn("sensor_id", df.columns)
        self.assertEqual(df.shape[0], 2)

    def test_prepare_date_column(self):
        df = pd.DataFrame({
            "store_location": ["A", "B"],
            "year": [2023, 2023],
            "month": [5, 5],
            "day": [1, 2],
            "visit_count": [100, 200]
        })
        df = prepare_date_column(df)
        self.assertIn("date", df.columns)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df["date"]))

    def test_aggregate_daily_visits(self):
        df = pd.DataFrame({
            "store_location": ["A", "A", "B", "B"],
            "sensor_id": [1, 1, 2, 2],
            "year": [2023, 2023, 2023, 2023],
            "month": [5, 5, 5, 5],
            "day": [1, 2, 1, 2],
            "visit_count": [100, 200, 300, 0]
        })
        df = prepare_date_column(df)
        df_agg = aggregate_daily_visits(df)
        self.assertTrue((df_agg["visit_count"] > 0).all())  # All visit_count should be > 0
        self.assertIn("day_of_week", df_agg.columns)

    def test_add_moving_average_and_change(self):
        df = pd.DataFrame({
            "store_location": ["A", "A", "B", "B"],
            "sensor_id": [1, 1, 2, 2],
            "year": [2023, 2023, 2023, 2023],
            "month": [5, 5, 5, 5],
            "day": [1, 2, 1, 2],
            "visit_count": [100, 200, 300, 0]
        })
        df = prepare_date_column(df)
        df_agg = aggregate_daily_visits(df)
        df_result = add_moving_average_and_change(df_agg)
        self.assertIn("moving_avg_4", df_result.columns)
        self.assertIn("pct_change", df_result.columns)
        self.assertFalse(df_result["moving_avg_4"].isna().all())

    def test_load_sensor_data_empty(self):
        # Test case for when no CSV files are found
        with patch("glob.glob", return_value=[]):
            df = load_sensor_data(path="data/raw/")
            self.assertTrue(df.empty)


if __name__ == "__main__":
    unittest.main()
