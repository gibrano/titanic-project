
import pandas as pd
import numpy as np
import logging
import boto3
import os

def load_data(**kwargs):
    data_path = "training/dataset/"
    df_train = pd.read_csv(data_path + "train.csv")
    logging.info('Data was loaded successfully!')
    return df_train.to_json(orient='split')

def create_training_dataset(**kwargs):

    titles_dict = {'Capt': 'Other',
               'Major': 'Other',
               'Jonkheer': 'Other',
               'Don': 'Other',
               'Sir': 'Other',
               'Dr': 'Other',
               'Rev': 'Other',
               'Countess': 'Other',
               'Dona': 'Other',
               'Mme': 'Mrs',
               'Mlle': 'Miss',
               'Ms': 'Miss',
               'Mr': 'Mr',
               'Mrs': 'Mrs',
               'Miss': 'Miss',
               'Master': 'Master',
               'Lady': 'Other'}

    ti = kwargs['ti']
    json_obj = ti.xcom_pull(task_ids='load_table')

    df = pd.read_json(json_obj, orient='split')

    df['Title'] = df.Name.str.extract('([A-Za-z]+)\.', expand=False)
    df['Title'] = df['Title'].map(titles_dict)
    df.Title.fillna('Mr', inplace=True)

    means = df.groupby('Title')['Age'].mean().to_dict()

    df.loc[df.Age.isna(),'Age'] = df['Title'].loc[df.Age.isna()].map(means)

    df = df.drop(['Name','Ticket', 'Cabin'], axis=1)
    df.Embarked = df.Embarked.fillna('S')

    df['FamilySize'] = df['SibSp'] + df['Parch']
    df.drop('SibSp',axis=1,inplace=True)
    df.drop('Parch',axis=1,inplace=True)

    embark_dummies_titanic  = pd.get_dummies(df['Embarked'])
    sex_dummies_titanic  = pd.get_dummies(df['Sex'])
    pclass_dummies_titanic  = pd.get_dummies(df['Pclass'], prefix="Class")
    title_dummies_titanic  = pd.get_dummies(df['Title'], prefix="Title")

    df = df.drop(['Embarked', 'Sex', 'Pclass', 'Title'], axis=1)
    df = df.join([embark_dummies_titanic, sex_dummies_titanic, pclass_dummies_titanic, title_dummies_titanic])

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
