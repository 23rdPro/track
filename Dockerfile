# syntax=docker/dockerfile:1

FROM python:3.7-alpine as base

FROM base as builder
=======
RUN python -m pip install --upgrade pip

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN python -m pip install --upgrade pip

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base

COPY --from=builder /install /usr/local
COPY src /track

WORKDIR /track

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip3 install -r requirements.txt

COPY . /track/
