# Running for example: docker build -f deploy/docker/Dockerfile -t project_dev .

FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/app/config && mkdir -p /logs /media /static

ADD requirements.txt /home/app/

RUN pip install -r /home/app/requirements.txt

COPY . /home/app/

WORKDIR /home/app/
