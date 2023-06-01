from datetime import datetime
from airflow import DAG
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.python_operator import PythonOperator
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 20),
}

with DAG('mysql_test_dag', default_args=default_args, schedule_interval=None) as dag:
    # Define your tasks
    check_mysql_connection = MySqlOperator(
        task_id='check_mysql_connection',
        mysql_conn_id='hrms',
        sql='SELECT 1;',
    )
    
    # Set task dependencies
    check_mysql_connection

# DAG level dependency
check_mysql_connection
