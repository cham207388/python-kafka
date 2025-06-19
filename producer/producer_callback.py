import logging

from confluent_kafka import Message

from producer.models import Student


class ProducerCallback:
    def __init__(self, student: Student):
        self.student = student
        self.logger = logging.getLogger(__name__)

    def __call__(self, err, msg: Message):
        if err:
            self.logger.error(
                f"❌ Failed to produce record: {self.student } {msg.key()}: {err}"
            )
        else:
            self.logger.info(
                f"✅ Record produced to topic: {msg.topic()}, partition: [{msg.partition()}] at offset: {msg.offset()}"
            )
