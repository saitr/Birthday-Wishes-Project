from datetime import datetime
from airflow import DAG
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.mysql_hook import MySqlHook


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 20),
}

def transform_data_function(**context):
    # Placeholder function for transformation logic
    # You can replace this function with your actual transformation code
    # Example: Print the transformed data
    from airflow.hooks.mysql_hook import MySqlHook
    mysql_hook = MySqlHook(mysql_conn_id='hrms')

    # Execute the SQL query
    sql_query = 'SELECT * FROM employee;'
    results = mysql_hook.get_records(sql_query)
    
    # Print the query results
    for row in results:
        print('this is the query of the employee table',row)

    # Example: Perform additional transformation logic
    transformed_data = "Transformed data"
    print(transformed_data)

def load_data_function(**context):
    # Placeholder function for data loading logic
    # You can replace this function with your actual loading code
    # Example: Perform database operation
    mysql_hook = MySqlHook(mysql_conn_id='hrms')

    # Example: Execute an INSERT statement
    insert_query = "INSERT INTO employee (employee_name, employee_email, employee_date_of_birth) VALUES ('John Doe', 'john.doe@example.com', '1985-02-15'), ('Jane Smith', 'jane.smith@example.com', '1990-09-21'), ('Michael Johnson', 'michael.johnson@example.com', '1988-07-07'), ('Emily Brown', 'emily.brown@example.com', '1995-04-12'),('William Davis', 'william.davis@example.com', '1982-11-30');"
    mysql_hook.run(insert_query)


with DAG('mysql_test_dag1', default_args=default_args, schedule_interval=None) as dag:
    # Define your tasks
    extract_data = MySqlOperator(
        task_id='extract_data',
        mysql_conn_id='hrms',
        sql='SELECT * FROM employee;',
        dag=dag
    )

    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data_function,
        provide_context=True,
        dag=dag
    )

    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_data_function,
        provide_context=True,
        dag=dag
    )

    # Set task dependencies
    extract_data >> transform_data >> load_data

