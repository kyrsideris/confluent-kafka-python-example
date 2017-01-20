import os
from time import gmtime, strftime, sleep
from confluent_kafka import Producer


def main():
    brokers = os.environ.get("KAFKA_BROKERS")
    topic = os.environ.get("KAFKA_TOPIC")
    # The period of time in milliseconds after which we force a refresh of
    # metadata even if we haven't seen any partition leadership changes to
    # proactively discover any new brokers or partitions.
    metadata_refresh_ms = 300000
    p = Producer({'bootstrap.servers': brokers,
                  'api.version.request': 'true',
                  'metadata.max.age.ms': metadata_refresh_ms    # for kafka 0.10
                  # 'topic.metadata.refresh.interval.ms': 1000  # for kafka 0.8
                  })

    while True:
        now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        p.produce(topic, now.encode('utf-8'))
        p.flush()
        sleep(1)

if __name__ == '__main__':
    main()
