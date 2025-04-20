from confluent_kafka import Producer
import json
import logging


class ProducerService:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.topic = topic
        self.producer = Producer({
            'bootstrap.servers': bootstrap_servers
        })
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def delivery_report(self, err, msg):
        if err is not None:
            self.logger.error(f"❌ Delivery failed for record {msg.key()}: {err}")
        else:
            self.logger.info(f"✅ Record produced to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")

    def produce(self, key: str, value: dict):
        try:
            self.logger.info(f"Producing to topic {self.topic}: {value}")
            self.producer.produce(
                topic=self.topic,
                key=key,
                value=json.dumps(value),
                callback=self.delivery_report
            )
            self.producer.poll(0)
        except BufferError as e:
            self.logger.error(f"❗ Local producer queue is full ({len(self.producer)} messages awaiting delivery): {e}")
        except Exception as e:
            self.logger.exception("Unexpected error while producing message")

    def flush(self):
        self.logger.info("🔄 Flushing remaining messages...")
        self.producer.flush()