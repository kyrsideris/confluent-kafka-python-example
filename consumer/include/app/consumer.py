import os
from confluent_kafka import Consumer, KafkaError


def main():
    brokers = os.environ.get("KAFKA_BROKERS")
    topics = os.environ.get("KAFKA_TOPICS").split(',')
    c = Consumer({'bootstrap.servers': brokers, 'group.id': 'consumer',
                  'api.version.request': 'true',
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
