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

def check_terraform_files():
    """Check if Terraform files exist"""
    terraform_dir = '/opt/airflow/terraform'
    if not os.path.exists(f'{terraform_dir}/main.tf'):
        raise FileNotFoundError(f"main.tf not found in {terraform_dir}")
    print(f"Terraform files found in {terraform_dir}")

dag = DAG(
    'terraform_automation',
    default_args=default_args,
    description='Automate Terraform infrastructure deployment',
    schedule_interval='@weekly',  # Change as needed: @hourly, @daily, @weekly, or cron expression
    catchup=False,
    tags=['terraform', 'infrastructure'],
)

# Task 1: Check Terraform files
check_files = PythonOperator(
    task_id='check_terraform_files',
    python_callable=check_terraform_files,
    dag=dag,
)

# Task 2: Terraform Init
terraform_init = BashOperator(
    task_id='terraform_init',
    bash_command='cd /opt/airflow/terraform && terraform init',
    dag=dag,
)

# Task 3: Terraform Validate
terraform_validate = BashOperator(
    task_id='terraform_validate',
    bash_command='cd /opt/airflow/terraform && terraform validate',
    dag=dag,
)

# Task 4: Terraform Plan
terraform_plan = BashOperator(
    task_id='terraform_plan',
    bash_command='cd /opt/airflow/terraform && terraform plan -out=tfplan',
    dag=dag,
)

# Task 5: Terraform Apply
terraform_apply = BashOperator(
    task_id='terraform_apply',
    bash_command='cd /opt/airflow/terraform && terraform apply -auto-approve tfplan',
    dag=dag,
)

# Task 6: Cleanup plan file
cleanup = BashOperator(
    task_id='cleanup_plan',
    bash_command='cd /opt/airflow/terraform && rm -f tfplan',
    dag=dag,
)

# Optional: Terraform Destroy (uncomment if needed)
# terraform_destroy = BashOperator(
#     task_id='terraform_destroy',
#     bash_command='cd /opt/airflow/terraform && terraform destroy -auto-approve',
#     dag=dag,
# )

# Define task dependencies
check_files >> terraform_init >> terraform_validate >> terraform_plan >> terraform_apply >> cleanup