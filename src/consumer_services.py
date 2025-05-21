import asyncio
import logging
import json
from aiokafka import AIOKafkaProducer
from aiokafka import AIOKafkaConsumer
from sqlmodel import Session

from models import Student
from schema_validator import StudentSchemaValidator
from utils import bootstrap_servers, kafka_topic, kafka_topic_dlt, consumer_group_id_dlt, consumer_group_id

class ConsumerServiceDLT:
    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            kafka_topic,
            bootstrap_servers=bootstrap_servers,
            group_id=consumer_group_id_dlt,
            enable_auto_commit=False
        )

    async def start(self):
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                await self.handle_dlt(msg)
        finally:
            await self.consumer.stop()
    async def handle_dlt(self, msg):
        try:
            data = json.loads(msg.value.decode("utf-8"))
            print(f"[DLT] Handling failed message: {data}")
            # Future: Send alert, store for manual inspection, etc.
            await self.consumer.commit()
        except Exception as e:
            print(f"[DLT] Failed to process DLT message: {e}")

class ConsumerService:
    def __init__(self, db_engine):
        self.consumer = AIOKafkaConsumer(
            kafka_topic,
            bootstrap_servers=bootstrap_servers,
            group_id=consumer_group_id,
            enable_auto_commit=False
        )
        self.dlt_producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)
        self.validator = StudentSchemaValidator()
        self.engine = db_engine
        self.logger = logging.getLogger(__name__)

    async def start(self):
        await self.dlt_producer.start() # for dlt
        await self.consumer.start()
        self.logger.info("Consumer started...")
        try:
            async for msg in self.consumer:
                await self.process_message(msg)
        finally:
            await self.consumer.stop()
            await self.dlt_producer.stop()

    async def process_message(self, msg, attempt: int = 1):
        try:
            data = json.loads(msg.value.decode("utf-8"))
            self.validator.validate_or_raise(data)

            student = Student(**data)
            with Session(self.engine) as session:
                session.add(student)
                session.commit()

            await self.consumer.commit()
            print(f"Committed offset for message: {data}")
        except Exception as e:
            print(f"Error processing message: {e}")
            if attempt < 3:
                await asyncio.sleep(1)
                await self.process_message(msg, attempt + 1)
            else:
                await self.dlt_producer.send_and_wait(kafka_topic_dlt, msg.value)
                await self.consumer.commit()
                print(f"Sent to DLT and committed offset: {msg.value}")
