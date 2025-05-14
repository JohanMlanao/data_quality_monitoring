import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="data_quality_monitoring",
    schedule="0 8 1 * *",
    catchup=False,
    start_date=datetime.datetime(2025,1,1),
    dagrun_timeout=datetime.timedelta(minutes=60),
) as dag:
    first_task = BashOperator(
        task_id="first_task",
        bash_command="python ~/data_quality_monitoring/extract_data.py"
    )

    second_task = BashOperator(
        task_id="second_task",
        bash_command="python ~/data_quality_monitoring/transform_data.py",
    )
    first_task >> second_task

if __name__ == "__main__":
    dag.test()
