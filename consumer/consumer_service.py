import logging
from confluent_kafka import KafkaException, Message, DeserializingConsumer
from sqlmodel import Session, select

from utils import engine
from models import deserialize, Student


class ConsumerService:
    def __init__(self, config, topic: str):
        self.topic = topic
        self.config = config
        self.consumer = DeserializingConsumer(self.config)
        self.consumer.subscribe([self.topic])
        self.logger = logging.getLogger(__name__)
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
                self.consumer.store_offsets(message)
        except KeyboardInterrupt:
            self.logger.info("👋 Consumer stopped.")
        finally:
            self.consumer.close()

    def handle_message(self, message: Message):
        key = message.key()
        partition = message.partition()
        offset = message.offset()
        value = message.value()
        try:
            # key = key.decode() if key else None
            student = deserialize(value)
            
            self.logger.info(f"📝 Received message with [key:{key}], from [partition:{partition}], at [offset:{offset}]")
            self.persist(student)

        except Exception as e:
            self.logger.error(f"❌ Failed to process message: {e}")
            
    def persist(self, student):
      with Session(engine) as session:
          existing = session.exec(select(Student).where(Student.id == student.id)).first()
          if existing:
              self.logger.info(f"⚠️ Student {student.id} already exists. Skipping insert.")
              return
          session.add(student)
          session.commit()
          self.logger.info('student saved to db!')
        