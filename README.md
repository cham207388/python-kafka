# 🐳 Kafka Producer & Consumer Service with Python

- [🐳 Kafka Producer \& Consumer Service with Python](#-kafka-producer--consumer-service-with-python)
  - [📦 Features](#-features)
    - [🚀 ProducerService](#-producerservice)
    - [🎯 ConsumerService](#-consumerservice)
  - [🧱 Project Structure](#-project-structure)
  - [⚙️ Requirements](#️-requirements)
  - [🧪 Running Locally](#-running-locally)
    - [Step 1: Start Kafka Cluster](#step-1-start-kafka-cluster)
    - [Step 2: Produce Messages](#step-2-produce-messages)
    - [Step 3: Consume Messages: one consumer](#step-3-consume-messages-one-consumer)
  - [🧠 Key Concepts](#-key-concepts)
  - [📌 Tips](#-tips)
  - [👷‍♂️ Future Enhancements](#️-future-enhancements)
  - [🧡 Resources](#-resources)
  - [Producer Configs](#producer-configs)
    - [General](#general)
    - [Advanced Reliability](#advanced-reliability)
    - [Authentication \& TLS](#authentication--tls)


This project demonstrates a Kafka-based message system using **Confluent Kafka Python Client**, featuring:

- ✅ A robust `ProducerService` that auto-creates compacted topics
- ✅ A scalable `ConsumerService` supporting consumer group parallelism
- ✅ Partitioning strategy based on UUID hash modulus
- ✅ Integration-ready with Docker Compose for local Kafka clusters

---

## 📦 Features

### 🚀 ProducerService
- Uses `confluent_kafka.Producer`
- Automatically creates topic if it does not exist (with `cleanup.policy=compact`)
- Accepts a UUID key, converts to int, and routes to 1 of 2 partitions based on modulo
- Delivery report logging
- Handles full buffer queue and retryable errors gracefully

### 🎯 ConsumerService
- Uses `confluent_kafka.Consumer`
- Supports scalable consumption via **consumer groups**
- Handles auto-rebalancing and partitions assignments
- Easy scaling: run multiple consumer instances to process in parallel

---

## 🧱 Project Structure

```bash
.
├── alembic/                      # database migration
│   └── env.py
│   └── versions/  
├── producer/
│   └── producer_service.py       # Kafka producer class with topic auto-creation
├── consumer/
│   └── consumer_service.py       # Kafka consumer class for consuming messages
├── confluent-compose-3b.yaml      # Full Kafka environment (multi-broker)
├── README.md                     # You are here 👋
```

---

## ⚙️ Requirements

- Python 3.12+
- Docker & Docker Compose
- `confluent-kafka` kafka
- `pydantic`, `sqlmodel` (optional, for model validation)
- `psycopg2-binary` PostgreSQL
- `python-dotenv` environment variable
- `alembic` db migration
- `mmh3` hasing

---

## 🧪 Running Locally

### Step 1: Start Kafka Cluster
```bash
docker compose -f docker-compose-kafka-full.yaml up -d
```

This sets up:
- 3 Kafka brokers (`broker1`, `broker2`, `broker3`)
- Schema Registry
- Kafka Connect
- Control Center
- ksqlDB, REST Proxy, Flink

### Step 2: Produce Messages
```python
from producer.producer_service import ProducerService
import uuid

producer = ProducerService(bootstrap_servers="localhost:9092", topic="students")

student = {
    "id": str(uuid.uuid4()),
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Johnson"
}

producer.send(student["id"], student)
```

### Step 3: Consume Messages: one consumer
```python
from consumer.consumer_service import ConsumerService

consumer = ConsumerService(
    bootstrap_servers="localhost:9092",
    topic="students",
    group_id="students-group"
)
consumer.consume_forever()
```

🌀 To run multiple consumers in the same group:
```python
def run_consumer_instance(instance_id):
    consumer = ConsumerService(
      bootstrap_servers=bootstrap_server,
      topic=kafka_topic,
      group_id=consumer_group
    )
    logger.info(f'🧵 Starting consumer {instance_id}')
    consumer.consume_forever()
    
# Start multiple consumer threads (2)
for i in range(2):
    t = threading.Thread(target=run_consumer_instance, args=(i,))
    t.start()
```

---

## 🧠 Key Concepts

- **Log Compaction**: Ensures only latest record per key is retained
- **Partition-aware Routing**: `uuid.UUID(id).int % 2` maps to 2 partitions
- **Consumer Group**: Each partition is handled by one consumer per group

---

## 📌 Tips

- Use `docker compose down -v` to fully clean up volumes
- Topic creation is automatic if not found
- Schema Registry and Connect are wired in for future Avro/Connector extensions

---

## 👷‍♂️ Future Enhancements

- Add Protobuf/Avro schema integration
- Add retry and DLQ topics
- Include Prometheus/Grafana monitoring

---

## 🧡 Resources

A whole bunch of credit to:
- [confluent-kafka-python](https://github.com/confluentinc/confluent-kafka-python)
- [Confluent Platform Docker images](https://hub.docker.com/u/confluentinc)
- [docker kafka](https://docs.confluent.io/platform/current/get-started/platform-quickstart.html)
- [confluent-kafka pypi](https://pypi.org/project/confluent-kafka/#description)
- [confluent-kafka-docs](https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html)
- [confluent-kafka-github](https://github.com/confluentinc/confluent-kafka-python)

## Producer Configs

### General

| key | Description |
|-----|-------------|
| bootstrap.servers | Comma-separated list of brokers (required) |
| client.id | Logical identifier for the producer |
| acks | Message durability. '0', '1', or 'all' |
| enable.idempotence | Ensures exactly-once delivery (set to True) |
| linger.ms | Delay to batch messages |
| batch.num.messages | Max messages to batch before sending |
| retries | Auto-retries on failure |
| retry.backoff.ms | Time between retries |
| compression.type | 'snappy', 'gzip', 'lz4', 'zstd' |
| max.in.flight.requests.per.connection | Controls reordering risk |

### Advanced Reliability

| key | Description |
|-----|-------------|
| queue.buffering.max.messages | Max messages in local queue |
| queue.buffering.max.kbytes | Max memory (KB) to buffer messages |
| delivery.timeout.ms | Timeout for message delivery (default: 30s) |
| request.timeout.ms | Broker response wait time |
| socket.timeout.ms | Timeout for network operations |

### Authentication & TLS

| key | Description |
|-----|-------------|
| security.protocol | PLAINTEXT, SASL_PLAINTEXT, SSL, etc. |
| ssl.ca.location | Path to CA file for verifying broker |
| sasl.username / sasl.password | For SASL auth |
