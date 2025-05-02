import logging
import threading

from fastapi import FastAPI
from src.producer.producer_route import ProducerController
from src.producer.producer_service import ProducerService
from src.producer.student_service import StudentService
from src.utils import kafka_topic, num_of_consumers
from src.config import producer_config, consumer_config
from src.consumer.main import run_consumer_instance

producer_service = ProducerService(
    config=producer_config,
    topic=kafka_topic
)
student_service = StudentService()
producer_controller = ProducerController(producer_service, student_service)

logger = logging.getLogger(__name__)

app = FastAPI(title="Python Kafka API")
app.include_router(producer_controller.router)

logger.info("Create consumers")
for i in range(num_of_consumers):
    t = threading.Thread(target=run_consumer_instance, args=(i,consumer_config,kafka_topic,))
    t.start()