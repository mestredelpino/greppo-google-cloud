# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

COPY . /vector-demo/

WORKDIR /vector-demo

RUN pip3 install -r requirements.txt

CMD ["greppo", "serve", "app-bq.py", "--host=0.0.0.0"]