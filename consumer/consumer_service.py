import json
import logging
from confluent_kafka import Consumer, KafkaException
from sqlmodel import Session
from utils import engine
from models import to_student


class ConsumerService:
    def __init__(self, bootstrap_servers: str, topic: str, group_id: str):
        self.topic = topic
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',  # Start from beginning if no offset
        })

        self.logger = logging.getLogger(__name__)

        self.consumer.subscribe([self.topic])
        self.logger.info(f"📡 Subscribed to topic: {self.topic}")

    def consume_forever(self):
        try:
            while True:
                msg = self.consumer.poll(1.0)  # timeout in seconds
                if msg is None:
                    continue
                if msg.error():
                    raise KafkaException(msg.error())

                self.handle_message(msg.key(), msg.value())
        except KeyboardInterrupt:
            self.logger.info("👋 Consumer stopped.")
        finally:
            self.consumer.close()

    def handle_message(self, key, value):
        self.logger.info(f'binary value: {value}')
        try:
            key = key.decode() if key else None
            student = to_student(value)
            
            self.logger.info(f"📝 Received student record [key={key}]: {student}")
            self.persist(student)

        except Exception as e:
            self.logger.error(f"❌ Failed to process message: {e}")
            
    def persist(self, student):
      with Session(engine) as session:
        session.add(student)
        session.commit()
        self.logger.info('student saved!')
        