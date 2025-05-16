# Data Quality Monitoring 

## Overview

This project simulates a real-world **data quality monitoring workflow** using a complete data pipeline. The pipeline automates data extraction, transformation, and visualization, providing insights into data quality issues.

## Live Demo

Check out the interactive Streamlit dashboard here:  
[Streamlit app](https://data-quality-monitoring-2025.streamlit.app/)

## Architecture

The pipeline consists of the following steps:

### 1. Simulated Company Database (FastAPI)
- A FastAPI backend mimics a real application exposing data via an API.

### 2. Data Extraction (Python + Pandas)
- Python scripts use `requests` and `pandas` to fetch and structure data.

### 3. Transformation and Storage (Pandas)
- Data is cleaned and stored efficiently using **Parquet format**

### 4. ETL Automation (Airflow)
- Apache Airflow orchestrates the Extract-Transform-Load process for automation.

### 5. Database Creation (DuckDB)
- Parquet data is loaded into DuckDB for efficient queryinq.

### 6. Interactive Visualization (Streamlit App)
- A Streamlit dashboard provides insights into data quality via dynamic charts.

⚠️ Due to slow response times from Render, manual extraction may be used during development.

---

## Tech Stack

- **FastAPI** — Simulated data source API  
- **Python & Pandas** — Data extraction, transformation, and storage  
- **Apache Airflow** — ETL orchestration and scheduling  
- **DuckDB** — Analytical database engine  
- **Streamlit** — Interactive dashboard for data quality visualization  

---

## Getting Started

### Prerequisites

- Python 3.8+  
- Docker (optional, for running Airflow and FastAPI)  
- `pip` package manager  

---

## 🛠️ Installation

### 1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/data_quality_monitoring.git
   cd data_quality_monitoring
   ```
   
### 2. Set up a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI simulated company database

```bash
uvicorn app:app --reload
```

### 5. Start AirFlow to automate ETL workflows
(Refer to airflow/README.MD or documentation)

### 6. Launch Streamlit app for interactive visualization
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```bash
data_quality_monitoring/
── src/                        # Streamlit app source code
│   ├── __init__.py
│   ├── app.py                  # FastAPI app entrypoint
│   ├── sensor.py               # Sensor class
│   └── store.py                # Store class
├── app/                        # Streamlit app source code
│   ├── __init__.py
│   ├── app.py                  # Main Streamlit app entrypoint
│   ├── homepage.py             # Homepage and navigation components
│   ├── visualisation.py        # Visualization components
│   └── design.py               # Styling and UI design components
│
├── etl/                        # ETL related scripts and workflows
│   ├── __init__.py
│   ├── automated_etl.py        # Automated ETL orchestration (e.g. Airflow DAGs)
│   ├── extract_data.py         # Data extraction logic
│   ├── manual_extract_data.py  # Manual extraction utilities
│   ├── transform_data.py       # Data transformation logic
│   └── manual_transform_data.py # Manual transformation utilities
│
├── data/                       # Data storage folder
│   ├── raw/                    # Raw data files (e.g. from API)
│   ├── processed/              # Cleaned/transformed data (Parquet, CSV, etc.)
│   ├── data.duckdb
│
├── tests/                      # Test suites
│   ├── test_extract_data.py
│   ├── test_manual_extract_data.py
│   ├── test_store.py
│   ├── test_transform_data.py
│   └── test_visit_sensor.py      
│
├── .streamlit/ 
│   └── config.toml                # Streamlit config files
│
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
└── venv/                       # Virtual environment (optional - usually gitignore)
```

---

## 💡 Contributing

Contributions are welcome! Feel free to open issues or pull requests if you want to add new exercises, fix bugs, or improve functionality.

---