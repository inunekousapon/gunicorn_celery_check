# syntax=docker/dockerfile:experimental
FROM python:3.7.4-slim-buster

WORKDIR /app

# aptの先を日本にする
RUN sed -i.bak -e "s%http://archive.ubuntu.com/ubuntu/%http://ftp.iij.ad.jp/pub/linux/ubuntu/archive/%g" /etc/apt/sources.list

RUN set -x \ 
    && apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends supervisor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/log/supervisor

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./app/ /app/
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf