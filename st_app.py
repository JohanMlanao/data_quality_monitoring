import logging
import os

import duckdb
import numpy as np
import pandas as pd
import streamlit as st


def create_database() -> None:
    """
    Ensures the existence of the 'data' directory and the DuckDB database file.

    This function performs the following checks and actions:
    - Creates the 'data' directory if it does not exist.
    - Checks for the existence of the 'data.duckdb' database file within the 'data' directory.
    - If the database file does not exist, it establishes a connection to DuckDB, creates the database and create the table from a pre-existing Parquet file ('data/processed/data.parquet').

    Logs errors if the 'data' directory is missing and when the database creation process occurs.

    Returns:
        None
    """
    if "data" not in os.listdir():
        logging.error(os.listdir())
        logging.error("creating folder data")
        os.mkdir("data")
    if "data.duckdb" not in os.listdir("data"):
        init_db = duckdb.connect(database="data/data.duckdb", read_only=False)
        init_db.execute(
            "CREATE TABLE IF NOT EXISTS data AS SELECT * FROM 'data/processed/data.parquet'"
        )


def get_sensor(current_sensor: str) -> pd.DataFrame:
    """
    Retrieves sensors matching the given ID.

    Args:
        current_sensor (str): ID of the sensor (e.g. 1-8).
            If empty, retrieves all sensors.

    Returns:
        pd.DataFrame: A DataFrame of sensors.
    """
    if current_sensor:
        select_sensor_query = (
            f"SELECT * FROM data WHERE current_sensor = '{current_sensor}'"
        )
    else:
        select_sensor_query = "SELECT * FROM data"
    user_sensor = (
        con.execute(select_sensor_query).df().sort_values("date").reset_index(drop=True)
    )
    return user_sensor


# Creation of the database
create_database()

# Connection to the database
con = duckdb.connect(database="data/data.duckdb", read_only=False)

# -- Set page config
app_title = "Data quality monitoring"

st.set_page_config(page_title=app_title)

# Title the app
st.title("Data quality monitoring")

# -- Set time by GPS or event
available_sensor_df = con.execute(
    "SELECT DISTINCT sensor_idcurrent_sensor FROM data"
).df()
sensor_id = st.selectbox(
    "Please select a sensor to view (optional).",
    np.sort(available_sensor_df["sensor_idcurrent_sensor"].unique()),
    index=None,
    placeholder="Select a sensor ID...",
)

sensor = get_sensor(current_sensor=sensor_id)
st.write(sensor)
