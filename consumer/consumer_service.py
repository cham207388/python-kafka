import logging
from confluent_kafka import Consumer, KafkaException, Message
from sqlmodel import Session
from utils import engine
from models import deserialize


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
                message: Message = self.consumer.poll(1.0)  # timeout in seconds
                if message is None:
                    continue
                if message.error():
                    raise KafkaException(message.error())

                self.handle_message(message)
        except KeyboardInterrupt:
            self.logger.info("👋 Consumer stopped.")
        finally:
            self.consumer.close()

    def handle_message(self, message: Message):
        key = message.key()
        value = message.value()
        partition = message.partition()
        offset = message.offset()
        try:
            key = key.decode() if key else None
            student = deserialize(value)
            
            self.logger.info(f"📝 Received message [key:{key}], [partition:{partition}], [offset:{offset}]")
            self.persist(student)

        except Exception as e:
            self.logger.error(f"❌ Failed to process message: {e}")
            
    def persist(self, student):
      with Session(engine) as session:
        session.add(student)
        session.commit()
        self.logger.info('student saved to db!')
        