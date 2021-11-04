# syntax=docker/dockerfile:1

FROM python:3.7-alpine

RUN python -m pip install --upgrade pip
#RUN pip install flake8
#COPY . .
#RUN flake8 --ignore=E501,F401 .

WORKDIR /track

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
#RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/track/wheels -r requirements.txt

#COPY ./entrypoint.sh .
#RUN sed -i 's/\r$//g' /usr/src/track/entrypoint.sh
#RUN chmod +x /usr/src/track/entrypoint.sh

COPY . /track/

#ENTRYPOINT ["/usr/src/track/entrypoint.sh"]
