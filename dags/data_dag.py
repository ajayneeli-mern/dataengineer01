from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

dag = DAG(
    "run_python_file",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
)

run_script = BashOperator(
    task_id="run_script",
    bash_command="python3 /opt/airflow/scripts/extract.py",
    dag=dag,
)

run_clean = BashOperator(
    task_id="run_clean",
    bash_command="python3 /opt/airflow/my_dbt/clean_csvs.py",
    dag=dag,
)

run_script>>run_clean