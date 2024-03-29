from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 6, 14),
    'email': ['yabir.canario@hotmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=15),
    'max_active_runs': 1,
    'concurrency': 1,
}

dag = DAG('bbc_exchangeRates_execution', default_args=default_args)

t1 = BashOperator(
    task_id='run_processData',
    bash_command='python /opt/airflow/scripts/processData.py {{ macros.ds_format(ds, "%Y-%m-%d", "%d/%m/%Y") }}',
    dag=dag)

t2 = BashOperator(
    task_id='run_upload_to_gcp',
    bash_command='python /opt/airflow/scripts/upload_to_gcp.py /tmp/credentials.json',
    dag=dag)

t1 >> t2