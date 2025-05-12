import logging
import threading

from consumer.utils import consumer_group
from consumer_service import ConsumerService
from utils import kafka_topic, consumer_config

logger = logging.getLogger(__name__)

def run_consumer_instance(instance_id):
    consumer = ConsumerService(kafka_topic, consumer_group)
    logger.info(f'🧵 Starting consumer {instance_id}')
    consumer.consume_forever()
    
# Start multiple consumer threads (2)
for i in range(2):
    t = threading.Thread(target=run_consumer_instance, args=(i,))
    t.start()