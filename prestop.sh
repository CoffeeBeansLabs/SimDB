#!/bin/bash
echo $HOSTNAME
cd kafka_2.13-2.6.0
./bin/kafka-consumer-groups.sh --zookeeper zookeeper.prod.svc.cluster.local:2181 --delete --group $HOSTNAME
