#!/bin/bash

aws s3 cp s3://mlflow-titanic/ . --recursive

mlflow models serve -m /opt/mlflow-titanic/mlruns/0/4984ff6e9e07409a88164278dc9f3763/artifacts/model -h 0.0.0.0 -p 5001

