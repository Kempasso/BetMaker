#!/bin/bash
filename="/conf/kafka/topics"
while IFS= read -r line
do
    /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --create --topic "$line" --partitions 1 --replication-factor 1
done < "$filename"