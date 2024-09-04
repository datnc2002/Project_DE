from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow import DAG
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.operators.bash import BashOperator
import logging
import csv

default_args = {
    'owner': 'congdat',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def mysql_to_hook():
    hook = MySqlHook(mysql_conn_id = "mysql_default")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from bai_test.hpg")
    with open("dags/get_hpg.txt", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
    cursor.close()
    conn.close()
    logging.info("Saved hpg data in text file get_orders.txt")

with DAG(
    dag_id='query_statement',
    default_args=default_args,
    description='Query data in MySQL',
    start_date=datetime(2024, 9, 2, 2),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id="mysql_to_hook",
        python_callable=mysql_to_hook,
    )
    task1

