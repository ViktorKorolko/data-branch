from airflow import DAG
import pandas as pd
from datetime import datetime
from airflow.operators.python_operator import PythonOperator

def load_dataset():
    df=pd.read_csv(r'/c/Users/Vik/airflow/dags/sales.csv', usecols=[0, 1, 2, 7])
    df.to_csv(r'/c/Users/Vik/airflow/dags/country_sales.csv', index = False)
def transform_save():
    df = pd.read_csv(r'/c/Users/Vik/airflow/dags/country_sales.csv')
    df['Transaction_date'] = pd.to_datetime(df.Transaction_date, infer_datetime_format = True)
    df['Transaction_date'] = df['Transaction_date'].dt.strftime('%Y-%m-%d')
    df.to_parquet(r'/c/Users/Vik/airflow/dags/sales.parquet')

dag = DAG(dag_id='example_dag',
          start_date=datetime(2022, 7, 20),
          description='example',
          schedule_interval='@once')

load_dataset = PythonOperator(task_id='load_part_of_csv_file',
                           python_callable=load_dataset,
                           dag=dag)
transform_save = PythonOperator(task_id='transform_date_and_save_dataset',
                               python_callable=transform_save,
                               dag=dag)

load_dataset >> transform_save
