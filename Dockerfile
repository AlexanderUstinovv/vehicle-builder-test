FROM python:3.8.8-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add build-base

RUN pip install --upgrade pip
COPY ./requirements/common.txt .
RUN pip install -r common.txt

# copy project
COPY app /usr/src/app