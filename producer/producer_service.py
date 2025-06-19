import logging

import mmh3
from confluent_kafka import SerializingProducer

from producer.models import Student
from producer.producer_callback import ProducerCallback


class ProducerService:
    def __init__(self, config: dict, topic: str):
        self.config = config
        self.topic = topic
        self.producer = SerializingProducer(self.config)
        self.logger = logging.getLogger(__name__)

    def send(self, key: str, value: Student, partition: int):
        try:
            self.logger.info(f"Producing record:{value} to topic: {self.topic}")
            self.producer.produce(
                topic=self.topic,
                key=key,
                value=value,
                partition=partition,
                on_delivery=ProducerCallback(value),
            )
            self.producer.flush()
        except BufferError as e:
            self.logger.error(
                f"❗ Local producer queue is full ({len(self.producer)} messages awaiting delivery): {e}"
            )
        except Exception:
            self.logger.exception("Unexpected error while producing message")

    def get_partition(self, key: str, num_partitions: int):
        key_bytes = key.encode("utf-8")
        hash_value = mmh3.hash(key_bytes, signed=False)
        return hash_value % num_partitions
