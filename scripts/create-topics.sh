#!/bin/sh

echo 'Waiting for Kafka to be ready...'
cub kafka-ready -b broker1:29092 1 60

echo 'Creating topics...'
kafka-topics --bootstrap-server broker1:29092,broker2:29092,broker3:29092 \
  --create \
  --topic "${KAFKA_TOPIC}" \
  --partitions "${NUM_OF_PARTITION}" \
  --replication-factor "${REPLICA_FACTORS}" \
  --config min.insync.replicas=2 \
  --config cleanup.policy=compact

kafka-topics --bootstrap-server broker1:29092,broker2:29092,broker3:29092 \
  --create \
  --topic "${KAFKA_TOPIC_DLT}" \
  --partitions "${NUM_OF_PARTITION}" \
  --replication-factor "${REPLICA_FACTORS}" \
  --config min.insync.replicas=2 \
  --config cleanup.policy=compact

echo 'Topics created successfully'
exit 0