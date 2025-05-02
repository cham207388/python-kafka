import logging

from src.consumer.consumer_service import ConsumerService

logger = logging.getLogger(__name__)

def run_consumer_instance(instance_id, config, topic):
    consumer = ConsumerService(config=config, topic=topic)
    logger.info(f'🧵 Creating consumer: {instance_id} for topic: {topic}')
    consumer.consume_forever()
