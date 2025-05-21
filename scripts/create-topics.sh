#!/bin/sh

set -e  # Exit immediately on error

echo 'Waiting for Kafka to be ready...'
cub kafka-ready -b broker1:29092 1 60

BROKERS="broker1:29092,broker2:29092,broker3:29092"

create_topic_if_not_exists() {
  topic_name=$1

  echo "Checking if topic '$topic_name' exists..."
  if kafka-topics --bootstrap-server $BROKERS --list | grep -q "^$topic_name$"; then
    echo "Topic '$topic_name' already exists. Skipping creation."
  else
    echo "Creating topic '$topic_name'..."
    kafka-topics --bootstrap-server $BROKERS \
      --create \
      --topic "$topic_name" \
      --partitions "$NUM_OF_PARTITION" \
      --replication-factor "$REPLICA_FACTORS" \
      --config min.insync.replicas=2 \
      --config cleanup.policy=compact
  fi
}

create_topic_if_not_exists "$KAFKA_TOPIC"
create_topic_if_not_exists "$KAFKA_TOPIC_DLT"

echo 'Topic initialization complete.'
exit 0