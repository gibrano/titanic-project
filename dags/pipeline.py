import datetime as dt
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from training.preprocessing import *
from training.train import run_models

default_args = {
    'owner': 'Gibran Otazo',
    'depends_on_past': False,
    'start_date': dt.datetime.strptime('2022-08-07T12:00:00', '%Y-%m-%dT%H:%M:%S'),
    'provide_context': True
}

dag = DAG('training_pipeline_dag', default_args=default_args, schedule_interval='0 9 * * 1') #, max_active_runs=1


load_table = PythonOperator(task_id='load_table', python_callable=load_data, op_kwargs={}, dag=dag)

train_data = PythonOperator(task_id='train_data', python_callable=create_training_dataset, op_kwargs={}, dag=dag)

run_models = PythonOperator(task_id='run_models', python_callable=run_models, op_kwargs={}, dag=dag)

upload_models = PythonOperator(task_id='upload_models', python_callable=upload_models, op_kwargs={}, dag=dag)

load_table.set_downstream(train_data)
train_data.set_downstream(run_models)
run_models.set_downstream(upload_models)

