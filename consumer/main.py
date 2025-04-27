import logging
import threading
from confluent_kafka import Producer
from consumer_service import ConsumerService
from utils import kafka_topic, kafka_topic_dlt, bootstrap_servers
from config import consumer_config, student_schema_dict
from retry_service import RetryService

dl_producer = Producer({"bootstrap.servers": bootstrap_servers})

retry_service = RetryService(
    dl_topic=kafka_topic_dlt,
    producer=dl_producer)

student_schema = student_schema_dict()

logger = logging.getLogger(__name__)
NUMBER_OF_CONSUMERS = 2


def run_consumer_instance(instance_id, config, topic):
    consumer = ConsumerService(
        config=config,
        topic=topic,
        schema=student_schema,
        retries=3,
        retry_service=retry_service
    )
    logger.info(f'🧵 Creating consumer: {instance_id} for topic: {topic}')
    consumer.consume_forever()


for i in range(NUMBER_OF_CONSUMERS):
    t = threading.Thread(target=run_consumer_instance, args=(i, consumer_config, kafka_topic,))
    t.start()
