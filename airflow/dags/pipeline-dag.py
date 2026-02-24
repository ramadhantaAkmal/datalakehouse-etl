import sys
import os

external_script_path = '/opt/airflow/lib'
sys.path.append(external_script_path)

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime
from pendulum import duration
from main import main
from job_matcher import run_job_matcher

with DAG(
    dag_id='pipeline-dag',
    start_date = datetime(2025,11,9),
    schedule= '@weekly',
    catchup=False,
    description='weekly scrape jobs',
    tags=['scrape','weekly'],
    default_args={"retries":1},
    dagrun_timeout=duration(minutes=20)

)as dag:
    scrape_task = PythonOperator(
        task_id='scrape_google_jobs',
        python_callable=main,
        provide_context=True
    )
    
    
    job_match_task = PythonOperator(
        task_id='job_matching_task',
        python_callable=run_job_matcher,
        provide_context=True
    )
    
    scrape_task >> job_match_task