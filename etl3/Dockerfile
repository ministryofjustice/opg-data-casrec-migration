FROM python:3.8-slim
RUN  apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y libpq-dev
RUN apt-get install -y postgresql-client
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt
COPY ./app /app
WORKDIR app
RUN chmod 755 stage_sirius_transform.sh
RUN chmod 755 app.py
RUN chmod 755 fixtures.py
CMD ["tail", "-f", "/dev/null"]
