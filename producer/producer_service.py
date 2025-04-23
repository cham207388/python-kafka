import json
import logging
import mmh3
from confluent_kafka import Message
from confluent_kafka.avro import AvroProducer

class ProducerService:
    def __init__(self, config: dict, value_schema, topic: str, dl_topic: str = None, dl_value_schema: str = None):
        self.topic = topic
        self.dl_topic = dl_topic
        self.value_schema = value_schema
        self.dl_value_schema = dl_value_schema
        self.producer = AvroProducer(config, default_value_schema=self.value_schema)
        self.logger = logging.getLogger(__name__)
        
    def delivery_report(self, err, message: Message):
        if err is not None:
            self.logger.error(f"❌ Delivery failed for record {message.key()}: {err}")
            self.send_to_dead_letter(message.key(), message.value(), str(err))
        else:
            self.logger.info(f"✅ Record produced to topic: {message.topic()}, partition: [{message.partition()}] @ offset: {message.offset()}")

    def send(self, key: str, value: dict, partition: int):
        try:
            self.logger.info(f"Producing record:{value} to topic: {self.topic}")
            self.producer.produce(
                topic=self.topic,
                key=key,
                value=value,
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

        Returns:
            None
        """
        self.logger.info("🔄 Flushing remaining messages...")
        self.producer.flush()
        
    def get_partition(self, key: str, num_partitions: int):
        key_bytes = key.encode("utf-8")
        hash_value = mmh3.hash(key_bytes, signed=False)
        return hash_value % num_partitions

    def send_to_dead_letter(self, key, value, error_msg):
        dl_value = json.dumps({
            "key": key.decode() if key else None,
            "original_value": value.decode() if value else None,
            "error": error_msg
        }).encode()

        self.producer.produce(self.dl_topic, key=key, value=dl_value)
        self.producer.flush()