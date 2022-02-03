FROM python:3.8-slim
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y libpq-dev
COPY requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt
