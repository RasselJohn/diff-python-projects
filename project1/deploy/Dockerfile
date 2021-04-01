# Running for example: docker build -f deploy/Dockerfile -t project .

FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /home/app && mkdir -p /var/project/static

ADD requirements.txt /home/app/

RUN pip install -r /home/app/requirements.txt

COPY . /home/app/

WORKDIR /home/app/
