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
    - [Step 3: Consume Messages:](#step-3-consume-messages)
  - [🧠 Key Concepts](#-key-concepts)
  - [📌 Tips](#-tips)
  - [👷‍♂️ Future Enhancements](#️-future-enhancements)
  - [🧡 Credits](#-credits)
  - [Gotchas](#gotchas)
    - [acks](#acks)
    - [enable.idempotence](#enableidempotence)
    - [max.in.flight.request.per.connection](#maxinflightrequestperconnection)


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
make dcu
```

This sets up:

- 3 Kafka brokers (`broker1`, `broker2`, `broker3`)
- Schema Registry
- Kafka Connect
- Control Center
- ksqlDB, REST Proxy, Flink

### Step 2: Produce Messages

```bash
make server
```

### Step 3: Consume Messages:

**one consumer**

```bash
make consumer
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

## 🧡 Credits

Built with ❤️ using:
- [confluent-kafka-python](https://github.com/confluentinc/confluent-kafka-python)
- [Confluent Platform Docker images](https://hub.docker.com/u/confluentinc)
- [docker kafka](https://docs.confluent.io/platform/current/get-started/platform-quickstart.html)
- [confluent-kafka pypi](https://pypi.org/project/confluent-kafka/#description)
- [confluent-kafka-docs](https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html)

## Gotchas

### acks
- acks = 0 (not guaranteed)
- acks = 1 (at least 1 data is written)
- acks = all (all data is written)

### enable.idempotence

- tell kafka to try resend
- if duplicate, kafka takes care of it

### max.in.flight.request.per.connection

- 1 (guarantees ordering)