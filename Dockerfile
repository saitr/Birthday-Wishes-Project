FROM apache/airflow:2.6.1

USER root

RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

RUN pip install --no-cache-dir mysql-connector-python

# Any other customizations or dependencies can be added here

CMD ["bash"]
