import logging
import threading
from consumer_service import ConsumerService
from utils import consumer_config, kafka_topic

logger = logging.getLogger(__name__)

def run_consumer_instance(instance_id):
    consumer = ConsumerService(config=consumer_config, topic=kafka_topic)
    logger.info(f'🧵 Starting consumer {instance_id}')
    consumer.consume_forever()
    
# Start multiple consumer threads (2)
for i in range(2):
    t = threading.Thread(target=run_consumer_instance, args=(i,))
    t.start()