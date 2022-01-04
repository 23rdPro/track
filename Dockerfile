# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /track

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install --upgrade pip \
    && pip install --default-timeout=100 -r requirements.txt


COPY . .

#RUN chmod +x /entrypoint.sh

ENV DJANGO_SETTINGS_MODULE track.settings

#ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000
