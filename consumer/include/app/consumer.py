import os
from confluent_kafka import Consumer, KafkaError


def main():
    brokers = os.environ.get("KAFKA_BROKERS")
    topics = os.environ.get("KAFKA_TOPICS").split(',')
    # The period of time in milliseconds after which we force a refresh of
    # metadata even if we haven't seen any partition leadership changes to
    # proactively discover any new brokers or partitions.
    metadata_refresh_ms = 300000
    c = Consumer({'bootstrap.servers': brokers, 'group.id': 'consumer',
                  'api.version.request': 'true',
                  'metadata.max.age.ms': metadata_refresh_ms,   # for kafka 0.10
                  # 'topic.metadata.refresh.interval.ms': 1000  # for kafka 0.8
                  'default.topic.config': {'auto.offset.reset': 'smallest'}})


    c.subscribe(topics)
    running = True
    while running:
        msg = c.poll()
        if not msg.error():
            print('Received message: %s' % msg.value().decode('utf-8'))
        elif msg.error().code() != KafkaError._PARTITION_EOF:
            print(msg.error())
            running = False
    c.close()

if __name__ == '__main__':
    main()
