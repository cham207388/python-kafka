import json
import logging
import uuid
from confluent_kafka import Producer

class ProducerService:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.topic = topic
        self.producer = Producer({
            'bootstrap.servers': bootstrap_servers
        })
        self.logger = logging.getLogger(__name__)

    def delivery_report(self, err, msg):
        if err is not None:
            self.logger.error(f"❌ Delivery failed for record {msg.key()}: {err}")
        else:
            self.logger.info(f"✅ Record produced to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")

    def send(self, key: str, value: dict):
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
        """
        Flushes any remaining messages in the producer buffer.

        This method logs an informational message indicating that the flushing process
        is starting and then calls the flush method on the producer to ensure all
        buffered messages are sent.

        The logger is used to provide a visual indication of the flushing process,
        and the producer's flush method is responsible for the actual transmission
        of messages.

        Returns:
            None
        """
        self.logger.info("🔄 Flushing remaining messages...")
        self.producer.flush()
        
    def get_part_key(self, uuid_str: str):
        int_key = uuid.UUID(uuid_str).int
        partition_key = str(int_key % 2)
        return f'part_{partition_key}'.encode('utf-8')