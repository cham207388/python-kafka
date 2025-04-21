import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from producer.producer_route import ProducerController
from producer.producer_service import ProducerService
from producer.student_service import StudentService
from producer.topic_service import TopicService
from producer.utils import bootstrap_server, kafka_topic


producer_service = ProducerService(bootstrap_servers=bootstrap_server, topic=kafka_topic)
student_service = StudentService()
topic_service = TopicService()
producer_controller = ProducerController(producer_service, student_service)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    topic_service.create_topic_if_not_exists(bootstrap_server, kafka_topic)
    yield  # The application is now running
    logger.info("Application shutdown complete!")

app = FastAPI(title="Python Kafka API", lifespan=lifespan)
app.include_router(producer_controller.router)