# Titanic Project

This project consists of two parts:

- The execution of an automated pipeline with Airflow and MlFlow.
- And an API in charge of making the predictions.

# Requirement

- AWS account with the enviroment variable AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.
- AWS S3 bucket.
- Docker and Docker Compose installed.

# Local deployment steps:

## Build the mlflow docker container

sudo docker build -t mlflow .

## Run docker-compose 

sudo AWS_ACCESS_KEY_ID='XXXXXXXXXXXXXXXXXXXXXXX' AWS_SECRET_ACCESS_KEY='XXXXXXXXXXXXXXXXXXXXXXXXXX' docker-compose up

# Airflow UI:

0.0.0.0:8080

![](./img/airflow.png)

Here you can execute the training pipeline and check logs. 

Note: The scheduler was configure to run weekly.

# MlFlow UI

0.0.0.0:5000

Here you can see the model versioning and the performance of each one.

![](./img/mlflow.png)

# Test the endpoint:

curl -X POST -H "Content-Type:application/json; format=pandas-split" --data '{"columns":["Age","SibSp","Parch","Fare","C","Q","S","female","male","Class_1","Class_2","Class_3"],"index":[1,2], "data":[[22.0,1,0,66.6,0,0,1,1,0,1,0,0],[30.0,0,1,40,0,0,1,1,0,1,0,0]]}' http://0.0.0.0:5001/invocations

# Monitor CPU and Memory with Grafana:

0.0.0.0:3000

![](./img/grafana.png)