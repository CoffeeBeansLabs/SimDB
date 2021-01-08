#!/bin/sh
#touch test
#echo $id > test
cd kafka_2.13-2.6.0
#bin/kafka-consumer-groups.sh --bootstrap-server kafka.prod.svc.cluster.local:9092  --delete --group $(<test)
bin/kafka-consumer-groups.sh --bootstrap-server kafka.prod.svc.cluster.local:9092  --delete --group $HOSTNAME
