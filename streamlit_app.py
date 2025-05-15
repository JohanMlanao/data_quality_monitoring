import os

import duckdb
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


def create_database() -> None:
    """
    This function performs the following checks and actions:
    - Checks for the existence of the 'data.duckdb' database file within the 'data' directory.
    - If the database file does not exist, it establishes a connection to DuckDB, creates the database and create the table from a pre-existing Parquet file ('data/processed/data.parquet').

    Returns:
        None
    """
    if "data.duckdb" not in os.listdir("data"):
        init_db = duckdb.connect(database="data/data.duckdb", read_only=False)
        init_db.execute(
            "CREATE TABLE IF NOT EXISTS data AS SELECT * FROM 'data/processed/data.parquet'"
        )


def get_table(current_store: str, current_sensor: str) -> pd.DataFrame:
    """
    Retrieves stores and sensors matching the given ID.

    Args:
        current_store (str): Location of the store (Bordeaux, Lyon, Marseille).
            If empty, retrieves all stores.
        current_sensor (str): ID of the sensor (e.g. 1-8).
            If empty, retrieves all sensors.

    Returns:
        pd.DataFrame: A DataFrame of specific stores and sensors.
    """
    if current_store and current_sensor:
        select_data_query = f"SELECT * FROM data WHERE store_location = '{current_store}' and sensor_id = '{current_sensor}'"
    elif current_store:
        select_data_query = (
            f"SELECT * FROM data WHERE store_location = '{current_store}'"
        )
    elif current_sensor:
        select_data_query = f"SELECT * FROM data WHERE sensor_id = '{current_sensor}'"
    else:
        select_data_query = "SELECT * FROM data"
    user_selection = (
        con.execute(select_data_query).df().sort_values("date").reset_index(drop=True)
    )
    return user_selection


# Creation of the database
create_database()

# Connection to the database
con = duckdb.connect(database="data/data.duckdb", read_only=False)

# -- Set page config
app_title = "Data quality monitoring"

st.set_page_config(page_title=app_title)

# Title the app
st.title("Data quality monitoring")

# Display the table and select a location and a sensor
available_location_df = con.execute(
    "SELECT DISTINCT store_location, sensor_id from data"
).df()
available_sensor_df = con.execute(
    "SELECT DISTINCT sensor_id FROM available_location_df"
).df()
with st.sidebar:
    location = st.selectbox(
        "Please select a location to view (optional).",
        np.sort(available_location_df["store_location"].unique()),
        index=None,
        placeholder="Select a location...",
    )
    sensor_id = st.selectbox(
        "Please select a sensor to view (optional).",
        np.sort(available_sensor_df["sensor_id"].unique()),
        index=None,
        placeholder="Select a sensor ID...",
    )

data = get_table(current_store=location, current_sensor=sensor_id)

# Display the sensor table
st.write(data)

data['legend_label'] = data['store_location'] + ' - ' + data['sensor_id']
# Display visit_count by date for each store
fig = px.line(data, x="date", y="visit_count", color="legend_label",
    title='Visitor Count Over Time by Location and Sensor')

fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Visitor Count',
    legend_title='Location - Sensor',
)

st.plotly_chart(fig, use_container_width=True)



# Display moving average by date for each store
fig = px.line(data, x="date", y="moving_avg_4", color="legend_label",
    title='Moving Average for each Day of the Week Over Time by Location and Sensor')

fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Moving Average',
    legend_title='Location - Sensor',
)

st.plotly_chart(fig, use_container_width=True)
