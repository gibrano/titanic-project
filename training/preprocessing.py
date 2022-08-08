
import pandas as pd
import logging
import boto3
import os

def load_data(**kwargs):
    data_path = "training/dataset/"
    df_train = pd.read_csv(data_path + "train.csv")
    logging.info('Data was loaded successfully!')
    return df_train.to_json(orient='split')

def create_training_dataset(**kwargs):
    ti = kwargs['ti']
    json_obj = ti.xcom_pull(task_ids='load_table')

    df = pd.read_json(json_obj, orient='split')

    df = df.drop(['Name','Ticket', 'Cabin'], axis=1)
    df.Age = df.Age.fillna(df.Age.median())
    df.Embarked = df.Embarked.fillna('S')

    embark_dummies_titanic  = pd.get_dummies(df['Embarked'])
    sex_dummies_titanic  = pd.get_dummies(df['Sex'])
    pclass_dummies_titanic  = pd.get_dummies(df['Pclass'], prefix="Class")

    df = df.drop(['Embarked', 'Sex', 'Pclass'], axis=1)
    df = df.join([embark_dummies_titanic, sex_dummies_titanic, pclass_dummies_titanic])

    return df.to_json(orient='split')

def upload_models(**kwargs):

    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

    bucket_name = "mlflow-titanic"
    s3 = boto3.client('s3')

    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-west-2'
    )

    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)

    path = './mlruns'

    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            bucket.upload_file(full_path,'mlruns/'+full_path[len(path)+1:])
