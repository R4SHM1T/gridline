from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'gridline_etl',
    default_args=default_args,
    description='A simple ETL DAG for Gridline',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    extract_raw = BashOperator(
        task_id='extract_raw',
        bash_command='python /path/to/ingestion/run_ingestion.py',
    )

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /path/to/dbt && dbt run',
    )

    extract_raw >> dbt_run
