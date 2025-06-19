import logging

from confluent_kafka import Producer


class RetryService:
    def __init__(self, producer: Producer, dl_topic: str):
        self.dl_topic = dl_topic
        self.producer = producer

        self.logger = logging.getLogger(__name__)

    def send_to_dlt(self, key, value_bytes):
        if not self.producer or not self.dl_topic:
            self.logger.warning("⚠️ No DLT configured, message lost.")
            return

        self.producer.produce(
            topic=self.dl_topic, key=key, value=value_bytes  # send raw bytes
        )
        self.producer.flush()
