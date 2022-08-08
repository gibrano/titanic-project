# FROM python:3.9-slim-buster

# RUN apt update
# RUN apt install awscli -y

# COPY requirements.txt /tmp
# RUN pip install -r /tmp/requirements.txt

# WORKDIR /opt/mlflow-titanic
# COPY serve_ui.sh .
# COPY serve_model.sh .

# RUN chmod +x serve_ui.sh
# RUN chmod +x serve_model.sh

# CMD ["./serve_ui.sh"]

FROM continuumio/miniconda3

# RUN conda install -c anaconda pandas
# RUN conda install -c anaconda numpy
# RUN conda install -c conda-forge mlflow
# RUN conda install -c anaconda scikit-learn
# RUN conda install -c anaconda boto3

RUN apt update
RUN apt install awscli -y

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

WORKDIR /opt/mlflow-titanic
COPY serve_ui.sh .
COPY serve_model.sh .

RUN chmod +x serve_ui.sh
RUN chmod +x serve_model.sh

CMD ["./serve_ui.sh"]