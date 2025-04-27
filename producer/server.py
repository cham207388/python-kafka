import logging

from fastapi import FastAPI

from producer.producer_route import ProducerController
from producer.producer_service import ProducerService
from producer.student_service import StudentService
from producer.utils import kafka_topic
from producer.config import producer_config, student_schema_dict

student_schema = student_schema_dict()

producer_service = ProducerService(
    config=producer_config,
    topic=kafka_topic,
    schema=student_schema
)
student_service = StudentService()
producer_controller = ProducerController(producer_service, student_service)

logger = logging.getLogger(__name__)

app = FastAPI(title="Python Kafka API")
app.include_router(producer_controller.router)
