FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ../config/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# copy web_run.sh
COPY deploy/scripts/web_run.sh .
RUN chmod +x  ./web_run.sh

COPY ../src /app/src
