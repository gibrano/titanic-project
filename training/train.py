import os
import warnings
import sys

import pandas as pd
import numpy as np
from sklearn import datasets

from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score 
from sklearn.model_selection import train_test_split

from urllib.parse import urlparse
import mlflow
import mlflow.sklearn

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def metrics(actual, pred):
    acc = accuracy_score(actual, pred)
    recall = recall_score(actual, pred)
    precision = precision_score(actual, pred)
    f1 = f1_score(actual, pred)
    return acc, recall, precision, f1

def run_models(**kwargs):

    ti = kwargs['ti']
    json_obj = ti.xcom_pull(task_ids='train_data')

    df = pd.read_json(json_obj, orient='split')
    X = df.drop('Survived', axis=1)
    X.set_index('PassengerId', inplace=True)

    y = df.Survived.values

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.20, random_state=1)
    logging.info('train_shape: %d , validation_shape: %d' % (len(X_train), len(X_val)))

    models = [('Linear SVC', LinearSVC()), ('Random Forest',RandomForestClassifier())]
    
    results = []
    names = []

    for name, model in models:
        with mlflow.start_run(run_name=name):

            model.fit(X_train, y_train)
            
            y_train_hat = model.predict(X_train)
            y_val_hat = model.predict(X_val)

            (train_accuracy, train_recall, train_precision, train_f1) = metrics(y_train, y_train_hat)
            (val_accuracy, val_recall, val_precision, val_f1) = metrics(y_val, y_val_hat)

            mlflow.sklearn.log_model(model, name)
            mlflow.log_metric("train_accuracy", train_accuracy)
            mlflow.log_metric("train_recall", train_recall)
            mlflow.log_metric("train_precision", train_precision)
            mlflow.log_metric("train_f1", train_f1)
            mlflow.log_metric("val_accuracy", val_accuracy)
            mlflow.log_metric("val_recall", val_recall)
            mlflow.log_metric("val_precision", val_precision)
            mlflow.log_metric("val_f1", val_f1)
                        
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            if tracking_url_type_store != "file":
                mlflow.sklearn.log_model(model, "model", registered_model_name=name)
            else:
                mlflow.sklearn.log_model(model, "model")