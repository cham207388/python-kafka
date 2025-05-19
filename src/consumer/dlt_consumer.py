import asyncio
import json
from aiokafka import AIOKafkaConsumer
from src.utils import bootstrap_servers, kafka_topic, consumer_group_id_dlt

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
