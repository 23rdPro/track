# syntax=docker/dockerfile:1

FROM python:3.7-alpine

RUN python -m pip install --upgrade pip

WORKDIR /track

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . /track/
