from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 6, 21),
    'email': ['yabir.canario@hotmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=15),
  }

dag = DAG('blablacar_test', default_args=default_args)


t1 = BashOperator(
    task_id='test_airflow',
    bash_command='echo {{ macros.ds_format(ds, "%Y-%m-%d", "%d/%m/%Y") }}',
    dag=dag)


