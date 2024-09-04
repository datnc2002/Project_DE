import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError

# Hàm để tạo bảng trong MySQL dựa trên cấu trúc của DataFrame
def create_table_from_df(engine, table_name, df):
    inspector = inspect(engine)
    # Xóa bảng nếu nó đã tồn tại để đảm bảo có bảng mới với cấu trúc đúng
    if inspector.has_table(table_name):
        engine.execute(f"DROP TABLE {table_name}")
    # Tạo bảng mới dựa trên DataFrame
    df.head(0).to_sql(table_name, engine, if_exists='replace', index=False)

# Hàm để import dữ liệu từ CSV vào MySQL
def import_csv_to_mysql(file_path, table_name, mysql_conn_id):
    # Khởi tạo MySqlHook
    mysql_hook = MySqlHook(mysql_conn_id=mysql_conn_id)
    engine = create_engine(mysql_hook.get_uri())

    # Đọc dữ liệu từ CSV
    df = pd.read_csv(file_path)
    logging.info(f"Read {len(df)} rows from {file_path}")

    # Tạo bảng mới trong MySQL dựa trên cấu trúc của DataFrame
    create_table_from_df(engine, table_name, df)

    # Nhập dữ liệu vào bảng
    df.to_sql(table_name, engine, if_exists='append', index=False)
    logging.info(f"Data from {file_path} inserted into {table_name}")

default_args = {
    'owner': 'congdat',
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
        'import_csv_to_mysql',
        default_args=default_args,
        description='Import CSV files to MySQL',
        schedule_interval='@daily',
        start_date=datetime(2024, 9, 2, 2),
        catchup=False,
) as dag:
    # Define file paths and corresponding table names
    files_and_tables = {
        '/opt/airflow/data/Nhan_vien.csv': 'Nhan_vien',
        '/opt/airflow/data/Khach_hang.csv': 'Khach_hang',
        '/opt/airflow/data/Chi_nhanh.csv': 'Chi_nhanh',
        '/opt/airflow/data/Du_lieu_ban_hang.csv': 'Du_lieu_ban_hang',
        '/opt/airflow/data/San_pham.csv': 'San_pham',
        '/opt/airflow/data/KPI_theo_nam.csv': 'KPI_theo_nam',
        # Thêm các file và bảng khác ở đây
    }

    for file_name, table_name in files_and_tables.items():
        import_csv = PythonOperator(
            task_id=f'import_csv_{table_name}',
            python_callable=import_csv_to_mysql,
            op_args=[file_name, table_name, 'mysql_default']
        )
        import_csv
