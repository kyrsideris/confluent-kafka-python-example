#Example of confluent-kafka use
Required `docker`

###Get the repo
Clone the repository into an `example` folder:
```bash
git clone https://github.com/kyrsideris/confluent-kafka-python-example.git example
```

###Setup the services
Bring up the environment:
```bash
docker-compose -f test.yml up 2>&1 | tee docker.log &
```

Check the state of the docker containers:
```bash
docker-compose -f test.yml ps
```
Output:
```bash
          Name                         Command               State                      Ports
----------------------------------------------------------------------------------------------------------------
example_consumer_1          /bin/sh -c python consumer ...   Up
example_kafka_1             start-kafka.sh                   Up       0.0.0.0:32784->9092/tcp
example_librdkafka-base_1   python2                          Exit 0
example_producer_1          /bin/sh -c python producer.py    Up
example_zookeeper_1         /docker-entrypoint.sh zkSe ...   Up       0.0.0.0:2181->2181/tcp, 2888/tcp, 3888/tcp
```

###Scale up the kafka
Scale the kafka service up to 3 containers:
```bash
docker-compose -f test.yml scale kafka=3
```

Check again the state:
```bash
$ docker-compose -f test.yml ps

          Name                         Command               State                      Ports
----------------------------------------------------------------------------------------------------------------
example_consumer_1          /bin/sh -c python consumer ...   Up
example_kafka_1             start-kafka.sh                   Up       0.0.0.0:32784->9092/tcp
example_kafka_2             start-kafka.sh                   Up       0.0.0.0:32785->9092/tcp
example_kafka_3             start-kafka.sh                   Up       0.0.0.0:32786->9092/tcp
example_librdkafka-base_1   python2                          Exit 0
example_producer_1          /bin/sh -c python producer.py    Up
example_zookeeper_1         /docker-entrypoint.sh zkSe ...   Up       0.0.0.0:2181->2181/tcp, 2888/tcp, 3888/tcp
```


###Gotcha
The python kafka client will not get the updated list immediately of brokers as the kafka clients are scaling up. The update rate of the broker list depends on the metadata refresh interval `metadata.max.age.ms` or `topic.metadata.refresh.interval.ms`.
So if we kill the master kafka container that was instantiated in the beginning before the metadata refresh interval, from the instantiation time, then the producer and consumer will fail.

Check the configuration properties: https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md

Kill the kafka master:
```bash
docker stop example_kafka_1
```

Check state:
```bash
docker-compose -f test.yml ps
...
example_kafka_1             start-kafka.sh                   Exit 0
...
```

In the log, the producer and consumer are complaining:
```bash
producer_1         | %3|1484908517.312|FAIL|rdkafka#producer-1| 4c71e483a7fc:9092/1001: Failed to resolve '4c71e483a7fc:9092': Name or service not known
producer_1         | %3|1484908517.312|ERROR|rdkafka#producer-1| 4c71e483a7fc:9092/1001: Failed to resolve '4c71e483a7fc:9092': Name or service not known
consumer_1         | %3|1484908517.313|FAIL|rdkafka#consumer-1| 4c71e483a7fc:9092/1001: Failed to resolve '4c71e483a7fc:9092': Name or service not known
consumer_1         | %3|1484908517.313|ERROR|rdkafka#consumer-1| 4c71e483a7fc:9092/1001: Failed to resolve '4c71e483a7fc:9092': Name or service not known
```

According to the `librdkafka` configuration documentation:
https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md

|  `metadata.max.age.ms`:  | `topic.metadata.refresh.interval.ms`: |
|:---------------------- |:---------------------- |
|  Metadata cache max age. Defaults to metadata.refresh.interval.ms * 3. Type: integer | Topic metadata refresh interval in milliseconds. The metadata is automatically refreshed on error and connect. Use -1 to disable the intervalled refresh. Type: integer |

This issue was discussed here:
https://github.com/confluentinc/confluent-kafka-python/issues/111

###Stop the services

Stop and remove the dockers containers:
```bash
docker-compose -f test.yml down
```

