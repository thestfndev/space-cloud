FROM python:3.10-slim

RUN apt-get update && apt-get upgrade

WORKDIR /app

RUN mkdir -p /app/storage/uploads

COPY ./app/requirements.txt .

RUN pip install -r requirements.txt

COPY ./app/ ./
