# Running for example: docker build -f deploy/docker/Dockerfile -t project_dev .

FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /home/app \
 && mkdir /home/app/config \
 && mkdir -p /logs \
 && mkdir -p /media \
 && mkdir -p /static

ADD requirements.txt /home/app/

RUN pip install -r /home/app/requirements.txt

COPY . /home/app/

WORKDIR /home/app/
