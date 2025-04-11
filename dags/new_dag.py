from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='cat_etl_pipeline',
    default_args=default_args,
    description='Pipeline gồm crawl, transform, save cat data',
    schedule_interval='0 9 * * *',  # 9h sáng hàng ngày
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['cat', 'etl'],
) as dag:

    crawl_cat = BashOperator(
        task_id='crawl_cat',
        bash_command='python /opt/airflow/app/crawl.py'
    )

    transform_cat = BashOperator(
        task_id='transform_cat',
        bash_command='python /opt/airflow/app/transform.py'
    )

    save_cat = BashOperator(
        task_id='save_cat',
        bash_command='python /opt/airflow/app/save.py'
    )

    crawl_cat >> transform_cat >> save_cat
