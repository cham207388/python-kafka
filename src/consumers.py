import logging
import asyncio

from consumer_services import ConsumerService, ConsumerServiceDLT
from utils import engine

logging.getLogger("aiokafka").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

async def start_main_consumer(instance_id):
    consumer = ConsumerService(db_engine=engine)
    logger.info(f'Creating consumer: {instance_id}')
    await consumer.start()

async def start_dlt_consumer():
    print("Starting DLT consumer")
    consumer = ConsumerServiceDLT()
    await consumer.start()

async def main():
    # Run 2 main consumers and 1 DLT consumer concurrently
    await asyncio.gather(
        start_main_consumer(1),
        start_main_consumer(2),
        start_dlt_consumer()
    )

if __name__ == "__main__":
    asyncio.run(main())
