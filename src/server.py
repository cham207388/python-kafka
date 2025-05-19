import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.schema_validator import StudentSchemaValidator
from src.producer.producer_route import ProducerController
from src.producer.producer_service import ProducerService
from src.producer.student_service import StudentService
from src.utils import kafka_topic, bootstrap_servers

schema_validator = StudentSchemaValidator()
producer_service = ProducerService(topic=kafka_topic,
                                   validator=schema_validator,
                                   bootstrap_servers=bootstrap_servers)
student_service = StudentService()
producer_controller = ProducerController(producer_service, student_service)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application started...")
    await producer_service.start()
    yield  # The application is now running
    logger.info("Application shutdown complete!")
    await producer_service.stop()

app = FastAPI(title="Python Kafka API", lifespan=lifespan)
app.include_router(producer_controller.router)
