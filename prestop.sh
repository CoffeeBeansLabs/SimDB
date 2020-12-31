#!/bin/bash
echo $HOSTNAME
cd kafka_2.13-2.6.0
bin/kafka-consumer-groups.sh --bootstrap-server kafka.prod.svc.cluster.local:9092  --delete --group $HOSTNAME
