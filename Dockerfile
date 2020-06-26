FROM python:alpine3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app
WORKDIR /app

RUN apk update && \
    apk add postgresql-dev gcc musl-dev libffi-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt
