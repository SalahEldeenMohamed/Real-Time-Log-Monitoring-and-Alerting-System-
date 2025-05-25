from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_engineer',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(dag_id='log_monitoring_pipeline',
         default_args=default_args,
         start_date=datetime(2025, 5, 20),
         schedule_interval='*/10 * * * *',
         catchup=False) as dag:

    start_log_producer = BashOperator(
        task_id='start_log_producer',
        bash_command='python3 /path/to/log_producer.py &',
        do_xcom_push=False
    )

    run_spark_job = BashOperator(
        task_id='run_log_processor',
        bash_command='spark-submit /path/to/log_processor.py'
    )

    check_alerts = BashOperator(
        task_id='check_alerts',
        bash_command='python3 /path/to/alert_checker.py'
    )

    cleanup_logs = BashOperator(
        task_id='cleanup_logs',
        bash_command='rm -rf /path/to/logs_output/*'
    )

    start_log_producer >> run_spark_job >> check_alerts >> cleanup_logs
