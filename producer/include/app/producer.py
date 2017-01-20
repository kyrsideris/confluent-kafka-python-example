import os
from time import gmtime, strftime, sleep
from confluent_kafka import Producer


def main():
    brokers = os.environ.get("KAFKA_BROKERS")
    topic = os.environ.get("KAFKA_TOPIC")
    p = Producer({'bootstrap.servers': brokers})

    while True:
        now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        p.produce(topic, now.encode('utf-8'))
        p.flush()
        sleep(1)

if __name__ == '__main__':
    main()
