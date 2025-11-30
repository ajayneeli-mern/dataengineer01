from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

DBT_PROJECT_DIR = "/opt/airflow/my_dbt"

def check_dbt_files():
    """Check if dbt project contains dbt_project.yml"""
    expected_file = f"{DBT_PROJECT_DIR}/dbt_project.yml"
    if not os.path.exists(expected_file):
        raise FileNotFoundError(f"{expected_file} not found.")
    print(f"dbt project exists: {expected_file}")

dag = DAG(
    'dbt_pipeline',
    default_args=default_args,
    description='Run dbt seeds and models automatically',
    schedule_interval='@daily',  # change: @hourly, @weekly, cron, etc.
    catchup=False,
    tags=['dbt', 'analytics'],
)

# Task 1: Validate files
check_files = PythonOperator(
    task_id='check_dbt_files',
    python_callable=check_dbt_files,
    dag=dag,
)

# Task 2: dbt debug
dbt_debug = BashOperator(
    task_id='dbt_debug',
    bash_command=f"cd {DBT_PROJECT_DIR} && dbt debug",
    dag=dag,
)

# Task 3: dbt seed
dbt_seed = BashOperator(
    task_id='dbt_seed',
    bash_command=f"cd {DBT_PROJECT_DIR} && dbt seed --full-refresh",
    dag=dag,
)

# Task 4: dbt run (build models)
dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command=f"cd {DBT_PROJECT_DIR} && dbt run",
    dag=dag,
)

# Task 5: dbt test (optional but recommended)
dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command=f"cd {DBT_PROJECT_DIR} && dbt test",
    dag=dag,
)

# DAG order
check_files >> dbt_debug >> dbt_seed >> dbt_run >> dbt_test
