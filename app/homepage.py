import streamlit as st
from design import page_header, show_footer

st.set_page_config(layout="wide")

# Title
page_header("Data Quality Monitoring", "An end-to-end pipeline for clean and reliable data")

# Project Overview
st.markdown("### 🧠 Project Overview")
st.markdown("""
This project demonstrates an end-to-end **data quality monitoring system** built using modern data engineering tools. It begins with a FastAPI-based simulated company database and progresses through an automated ETL process to deliver interactive dashboards via Streamlit.
""")

# Project Goal
st.markdown("### 🎯 Project Goal")
st.write("To proactively monitor and maintain data quality through an automated and interactive pipeline.")

# Tools & Technologies
st.markdown("### 🛠️ Tools & Technologies Used")
cols = st.columns(6)
tools = {
    "FastAPI": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
    "Python": "https://www.python.org/static/community_logos/python-logo.png",
    "Pandas": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Pandas_logo.svg/768px-Pandas_logo.svg.png",
    "Airflow": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/AirflowLogo.png/1200px-AirflowLogo.png",
    "DuckDB": "https://duckdb.org/images/logo-dl/DuckDB_Logo-horizontal.svg",
    "Streamlit": "https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png",
}

for col, logo_url in zip(cols, tools.values()):
    col.image(logo_url, width=100)

# Data Pipeline
st.markdown("### 🔄 Data Pipeline")

st.markdown("""
This project simulates a real-world data quality monitoring workflow using a complete data pipeline. Below is an overview of each step in the pipeline:

1. **Simulated Company Database (FastAPI)**  
   The project starts with a `FastAPI` backend designed to simulate a company’s data source. It mimics how a real application would expose its data via an API.

2. **Data Extraction (Python + Pandas)**  
   Python scripts interact with the API to fetch data. These scripts use `requests` and `pandas` to retrieve and parse the data into structured dataframes.

3. **Transformation and Storage (Pandas)**  
   The extracted data is cleaned and transformed using `pandas`. Final datasets are saved as efficient Parquet files.

4. **ETL Automation (Airflow)**  
   The entire Extract-Transform-Load process is orchestrated and scheduled using `Apache Airflow`, ensuring repeatability and automation.
   
5. **Database Creation (DuckDB)**  
   After automation, the Parquet data is loaded into a local analytical database using `DuckDB`, enabling efficient querying and integration with the dashboard.

6. **Interactive Visualization (Streamlit App)**  
   Finally, the processed data is loaded into a `Streamlit` app where users can explore data quality insights via dynamic charts and dashboards.

⚠️ Due to slow response times from Render, manual extraction is occasionally used to speed up the visualization process during development.
""")



show_footer()
