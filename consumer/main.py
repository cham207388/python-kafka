import logging
import threading

from consumer_service import ConsumerService
from utils import consumer_config, kafka_topic

logger = logging.getLogger(__name__)
NUMBER_OF_CONSUMERS = 2

def run_consumer_instance(instance_id, config, topic):
    consumer = ConsumerService(config=config, topic=topic)
    logger.info(f'🧵 Creating consumer: {instance_id} for topic: {topic}')
    consumer.consume_forever()

for i in range(NUMBER_OF_CONSUMERS):
    t = threading.Thread(target=run_consumer_instance, args=(i,consumer_config,kafka_topic,))
    t.start()
