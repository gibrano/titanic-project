#!/bin/bash

aws s3 cp s3://mlflow-titanic/ . --recursive

#mlflow server --default-artifact-root s3://mlflow-titanic -h 0.0.0.0

mlflow server --default-artifact-root /opt/mlflow-titanic -h 0.0.0.0

