from datetime import datetime
from airflow import DAG
from airflow.operators.email_operator import EmailOperator

default_args = {
    'owner': 'DollarBird',
    'start_date': datetime(2023, 5, 20),
}

