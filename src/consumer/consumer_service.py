import asyncio
import json
from sqlmodel import Session
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from src.utils import bootstrap_servers, kafka_topic, kafka_topic_dlt, consumer_group_id
from src.schema_validator import StudentSchemaValidator
from src.models import Student


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

    async def start(self):
        await self.dlt_producer.start() # for dlt
        await self.consumer.start()
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
