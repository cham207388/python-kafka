import logging
import json
from aiokafka import AIOKafkaProducer


class ProducerService:
    def __init__(self, topic: str, validator, bootstrap_servers):
        self.topic = topic
        self.validator = validator
        self.bootstrap_servers = bootstrap_servers
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        self.logger = logging.getLogger(__name__)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def produce(self, student_data: dict):
        try:
            self.validator.validate_or_raise(student_data)
            await self.producer.send_and_wait(self.topic, json.dumps(student_data).encode("utf-8"))
            print(f"Produced message to {self.topic}: {student_data}")
        except Exception as e:
            print(f"Failed to produce message: {e}")

