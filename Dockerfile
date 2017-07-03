FROM ubuntu:14.04
RUN apt-get update && apt-get install -y -q curl python-dev \
    libreadline-dev libbz2-dev libssl-dev libsqlite3-dev git wget \
    libxml2-dev libxslt1-dev python-pip build-essential automake libtool \
    libffi-dev libgmp-dev pkg-config libpq-dev postgresql-client

ADD requirements.txt /tmp/requirements.txt
RUN pip install -qr /tmp/requirements.txt

RUN mkdir -p /root/var/run/celery

COPY . /gnosisdb/
WORKDIR /gnosisdb
