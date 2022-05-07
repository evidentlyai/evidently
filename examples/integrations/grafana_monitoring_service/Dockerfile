# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY metrics_app/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN pip3 install evidently

COPY metrics_app .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8085"]