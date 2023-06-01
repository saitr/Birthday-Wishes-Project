from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_birthday_emails():
    # Connecting to the MySQL database using the MySqlOperator
    query = "SELECT employee_email, employee_name FROM employee WHERE DATE_FORMAT(employee_date_of_birth, '%m-%d') = DATE_FORMAT(NOW(), '%m-%d')"
    task = MySqlOperator(
        task_id='get_employee_emails',
        mysql_conn_id='hrms',
        sql=query,
        dag=dag
    )
    employee_data = task.execute(context={})
    # image_path = 'https://drive.google.com/file/d/1eXfjKyL6smHM3AjTYPIrmP-1moyvzdJC/view?usp=sharing'

    image_data = 'https://res.cloudinary.com/djgayxkbm/image/upload/v1685503643/birthday_image-PhotoRoom_zzspg9.png'
    # Get the base64-encoded image string

    if employee_data:
        # Email configuration
        smtp_host = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = 'saitreddy06@gmail.com'
        smtp_password = 'rndmsnlspighpxjj'
        from_email = 'saitreddy06@gmail.com'

        # Send emails to employees
        for employee_email, employee_name in employee_data:
            subject = 'Happy Birthday!'

            # Create the email content
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = employee_email
            msg['Subject'] = subject

            # Define the HTML template
            template = """
            <html>
            <body>
                <div style="background-image: url('{image_data}');
                            width: 100%;
                            background-repeat: no-repeat;
                            height: 100vh;
                            position:relative">
                    <h1 style="color: white;
                font-size: xx-large;
                font-weight: bold;
                font-size: 7vh;
                font-family: monospace;
                margin:0;
                padding-top: 28%;
                padding-left: 16%;">{employee_name}</h1>
                </div>
            </body>
            </html>
            """.format(image_data=image_data, employee_name=employee_name)

            # Attach the email content as HTML
            msg.attach(MIMEText(template, 'html'))

            # Connect to the SMTP server and send the email
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            server.quit()


# DAG
dag = DAG(
    dag_id='birthday_email_dag',
    start_date=datetime(2023, 5, 26),
    schedule_interval='@daily'
)

send_email_task = PythonOperator(
    task_id='send_birthday_emails',
    python_callable=send_birthday_emails,
    dag=dag
)
