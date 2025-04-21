import logging
import threading
from consumer_service import ConsumerService
from utils import bootstrap_server, kafka_topic, consumer_group

logger = logging.getLogger(__name__)

def run_consumer_instance(instance_id):
    consumer = ConsumerService(
      bootstrap_servers=bootstrap_server,
      topic=kafka_topic,
      group_id=consumer_group
    )
    logger.info(f'🧵 Starting consumer {instance_id}')
    consumer.consume_forever()
    
# Start multiple consumer threads (2)
for i in range(2):
    t = threading.Thread(target=run_consumer_instance, args=(i,))
    t.start()