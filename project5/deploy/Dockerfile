# Running for example: docker build -f deploy/docker/Dockerfile -t temperature .

FROM rust:1.48 as builder

RUN mkdir /home/app

COPY . /home/app/

WORKDIR /home/app/

RUN cargo build