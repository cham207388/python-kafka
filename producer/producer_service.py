import json
import logging
import mmh3
from confluent_kafka import Message, SerializingProducer

class ProducerService:
    def __init__(self,
                 config: dict,
                 topic: str):
        self.topic = topic

        self.producer = SerializingProducer(config)
        self.logger = logging.getLogger(__name__)
        
    def delivery_report(self, err, message: Message):
        if err is not None:
            self.logger.error(f"❌ Delivery failed for record {message.key()}: {err}")
        else:
            self.logger.info(f"✅ Record produced to topic: {message.topic()}, partition: [{message.partition()}] @ offset: {message.offset()}")

    def send(self, key: str, value: dict, partition: int):
        try:
            self.logger.info(f"Producing record:{value} to topic: {self.topic}")
            self.producer.produce(
                topic=self.topic,
                key=key,
                value=value,
                partition=partition,
                on_delivery=self.delivery_report
            )
            self.producer.poll(0)
        except BufferError as e:
            self.logger.error(f"❗ Local producer queue is full ({len(self.producer)} messages awaiting delivery): {e}")
        except Exception as e:
            self.logger.exception("Unexpected error while producing message")

    def flush(self):
        """
        Flushes any remaining messages in the producer buffer.

        Returns:
            None
        """
        self.logger.info("🔄 Flushing remaining messages...")
        self.producer.flush()
        
    def get_partition(self, key: str, num_partitions: int):
        key_bytes = key.encode("utf-8")
        hash_value = mmh3.hash(key_bytes, signed=False)
        return hash_value % num_partitions
