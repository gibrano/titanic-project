#!/bin/bash

aws s3 cp s3://mlflow-titanic/ . --recursive

mlflow models serve -m /opt/mlflow-titanic/mlruns/0/ab35436452ca4062b4be60a255aa2c50/artifacts/model -h 0.0.0.0 -p 5001

