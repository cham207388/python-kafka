# 🧰 Kafka CLI Command Reference

## 🛠️ Setup

```bash
# Enter the Kafka container
docker exec -it kafka1 bash

# Kafka CLI tool directory (usually included in PATH inside the container)
cd /bin
```

---

## 📋 Topic Management

| Task                          | Command |
|------------------------------|---------|
| **List all topics**          | `kafka-topics --bootstrap-server kafka1:19092 --list` |
| **Create a topic**           | `kafka-topics --bootstrap-server kafka1:19092 --create --topic my-topic --partitions 1 --replication-factor 1` |
| **Delete a topic**           | `kafka-topics --bootstrap-server kafka1:19092 --delete --topic my-topic` |
| **Describe a topic**         | `kafka-topics --bootstrap-server kafka1:19092 --describe --topic my-topic` |

---

## 📨 Produce Messages

| Task                          | Command |
|------------------------------|---------|
| **Start interactive producer** | `kafka-console-producer --broker-list kafka1:19092 --topic my-topic` |
| **Send JSON message from terminal** | Type message after running the command above:<br>`{"id": 1, "name": "John Doe"}` then press `Enter` |

---

## 📬 Consume Messages

| Task                          | Command |
|------------------------------|---------|
| **Start console consumer**   | `kafka-console-consumer --bootstrap-server kafka1:19092 --topic my-topic --from-beginning` |
| **Consume latest messages**  | `kafka-console-consumer --bootstrap-server kafka1:19092 --topic my-topic` |

---

## 🧪 Testing and Utilities

| Task                          | Command |
|------------------------------|---------|
| **Check Kafka broker status**| `kafka-broker-api-versions --bootstrap-server kafka1:19092` |
| **List consumer groups**     | `kafka-consumer-groups --bootstrap-server kafka1:19092 --list` |
| **Describe a consumer group**| `kafka-consumer-groups --bootstrap-server kafka1:19092 --describe --group my-group` |
| **Reset consumer group offset** | `kafka-consumer-groups --bootstrap-server kafka1:19092 --group my-group --topic my-topic --reset-offsets --to-earliest --execute` |

---

## 🔄 Kafka Config

| Task                          | Command |
|------------------------------|---------|
| **Get broker config**        | `kafka-configs --bootstrap-server kafka1:19092 --entity-type brokers --entity-name 1 --describe` |
| **Change topic retention**   | `kafka-configs --bootstrap-server kafka1:19092 --entity-type topics --entity-name my-topic --alter --add-config retention.ms=60000` |