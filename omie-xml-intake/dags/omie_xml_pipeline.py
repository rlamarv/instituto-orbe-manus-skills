from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from app.main import run_pipeline

with DAG(
    dag_id="omie_xml_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["omie", "xml", "contas-receber"],
) as dag:
    run_omie_xml_pipeline = PythonOperator(
        task_id="run_omie_xml_pipeline",
        python_callable=run_pipeline,
    )
