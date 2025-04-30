import io
import logging
import time
from confluent_kafka import KafkaException, Message, Consumer
from fastavro import parse_schema, schemaless_reader
from sqlmodel import Session, select

from retry_service import RetryService
from utils import engine
from models import deserialize, Student


class ConsumerService:
    def __init__(self, config,
                 topic: str,
                 schema: dict,
                 retries: int,
                 retry_service: RetryService,
                 retry_backoff: float = 1.0):
        self.topic = topic
        self.config = config
        self.schema = parse_schema(schema)
        self.retries = retries
        self.retry_service = retry_service
        self.retry_backoff = retry_backoff
        self.consumer = Consumer(self.config)
        self.consumer.subscribe([self.topic])

        self.logger = logging.getLogger(__name__)
        self.logger.info(f"📡 Subscribed to topic: {self.topic}")

    def _deserialize_avro(self, data: bytes) -> dict:
        """Manually deserialize Avro bytes to dict."""
        bytes_reader = io.BytesIO(data)
        return schemaless_reader(bytes_reader, self.schema)

    def consume_forever(self):
        try:
            while True:
                message: Message = self.consumer.poll(1.0)  # timeout in seconds
                if message is None:
                    continue
                if message.error():
                    self.logger.error(f"❌ Consumer error: {message.error()}")
                    raise KafkaException(message.error())

                key = message.key().decode() if message.key() else None
                partition = message.partition()
                offset = message.offset()
                value = self._deserialize_avro(message.value())

                success = False
                attempt = 0
                while attempt < self.retries:
                    try:
                        self.handle_message(key, value, partition, offset)
                        success = True
                        break
                    except Exception as e:
                        self.logger.warning(f"⚠️ Processing failed (attempt {attempt+1}/{self.retries}): {e}")
                        attempt += 1
                        time.sleep(self.retry_backoff * attempt)  # exponential backoff

                if not success:
                    self.logger.error(f"❌ Moving message to DLT after {self.retries} retries")
                    self.retry_service.send_to_dlt(key, message.value())
                # self.consumer.commit(asynchronous=False)
                self.consumer.store_offsets(message)

        except KeyboardInterrupt:
            self.logger.info("👋 Consumer stopped.")
        finally:
            self.consumer.close()

    def handle_message(self, key, value, partition, offset):

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
        