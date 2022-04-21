# Running for example: docker build -f deploy/docker/Dockerfile -t project_dev .

FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/app/config

COPY config/requirements.txt /home/app/config

RUN pip install -r /home/app/config/requirements.txt

COPY . /home/app/

WORKDIR /home/app/
