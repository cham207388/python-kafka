import logging
from fastapi import FastAPI

from producer.producer_route import ProducerController
from producer.producer_service import ProducerService
from producer.student_service import StudentService
from producer.topic_service import TopicService
from producer.utils import bootstrap_server, kafka_topic


producer_service = ProducerService(bootstrap_servers=bootstrap_server, topic=kafka_topic)
student_service = StudentService()
producer_controller = ProducerController(producer_service, student_service)

logger = logging.getLogger(__name__)

app = FastAPI(title="Python Kafka API")
app.include_router(producer_controller.router)