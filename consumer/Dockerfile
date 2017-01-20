FROM librdkafka-base:test

MAINTAINER kyrsideris

WORKDIR /app

ADD include/app/consumer.py /app/consumer.py

CMD python consumer.py 2>&1 | tee consumer.log