from datetime import datetime
from airflow import DAG
from airflow.operators.email_operator import EmailOperator

default_args = {
    'owner': 'sai',
    'start_date': datetime(2023, 5, 20),
}

with DAG('smtp_test_dag', default_args=default_args, schedule_interval=None) as dag:
    send_email = EmailOperator(
        task_id='send_email',
        to='rashmi.hk@dollarbirdinc.com',
        subject='Test Email',
        html_content='<p>This is a test email sent from Airflow using SMTP.</p>',
    )

    send_email
