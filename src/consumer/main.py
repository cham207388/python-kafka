import logging
import threading

from confluent_kafka import Producer

from src.config import consumer_config, student_schema_dict
from src.consumer.consumer_service import ConsumerService
from src.consumer.retry_service import RetryService
from src.utils import bootstrap_servers, kafka_topic, kafka_topic_dlt, num_of_consumers

dl_producer = Producer({"bootstrap.servers": bootstrap_servers})

retry_service = RetryService(dl_topic=kafka_topic_dlt, producer=dl_producer)

student_schema = student_schema_dict()

logger = logging.getLogger(__name__)


def run_consumer_instance(instance_id, config, topic):
    consumer = ConsumerService(
        config=config,
        topic=topic,
        schema=student_schema,
        retries=3,
        retry_service=retry_service,
    )
    logger.info(f"🧵 Creating consumer: {instance_id} for topic: {topic}")
    consumer.consume_forever()


for i in range(num_of_consumers):
    t = threading.Thread(
        target=run_consumer_instance,
        args=(
            i,
            consumer_config,
            kafka_topic,
        ),
    )
    t.start()
