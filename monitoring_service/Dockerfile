# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

RUN apt update && apt install -y git

COPY requirements.txt requirements.txt
COPY evidently-*.tar.gz ./


RUN pip3 install -r requirements.txt
COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]