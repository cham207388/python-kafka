import json
import logging
import mmh3
from confluent_kafka import Producer, Message

class ProducerService:
    def __init__(self, config: str, topic: str):
        self.topic = topic
        self.producer = self.create_producer(config)
        self.logger = logging.getLogger(__name__)
        
    def create_producer(self, config):
        producer = Producer(config)
        return producer
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
                value=json.dumps(value),
                callback=self.delivery_report,
                partition=partition
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
        
    def get_partition(self, id: str, num_partitions: int):
        key_bytes = id.encode("utf-8")
        hash_value = mmh3.hash(key_bytes, signed=False)
        return hash_value % num_partitions