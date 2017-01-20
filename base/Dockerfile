FROM python:2.7.13-slim

MAINTAINER kyrsideris

WORKDIR /tmp

### Kafka dependencies ###

RUN apt-get update
RUN apt-get install -y curl gcc g++ make \
    && curl -L https://github.com/edenhill/librdkafka/archive/v0.9.2-RC1.tar.gz | tar xzf - \
    && cd librdkafka-0.9.2-RC1/ \
    && ./configure --prefix=/usr \
    && make -j \
    && make install

RUN pip install 'confluent-kafka==0.9.2'

WORKDIR /app/

