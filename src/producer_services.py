import json
import asyncio
from aiokafka import AIOKafkaProducer
from sqlmodel import Session, select

from src.models import Student
from src.utils import engine
from fastapi import APIRouter
import uuid
import logging
from faker import Faker
fake = Faker()


class ProducerService:
    def __init__(self, topic: str, validator, bootstrap_servers):
        self.topic = topic
        self.validator = validator
        self.bootstrap_servers = bootstrap_servers
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        self.logger = logging.getLogger(__name__)

    async def start(self):
        self.logger.info("Producer starting...")
        await self.producer.start()

        # Force metadata update to avoid UnknownError
        self.logger.info("Waiting for Kafka metadata...")
        await self.producer.client.force_metadata_update()
        topics = self.producer.client.cluster.topics()
        if self.topic not in topics:
            self.logger.warning(f"Topic '{self.topic}' not found in metadata: {topics}")
        else:
            self.logger.info(f"Topic '{self.topic}' is available.")

        self.logger.info("Producer started...")

    async def stop(self):
        self.logger.info("Producer stopping...")
        await self.producer.stop()
        self.logger.info("Producer stopped...")

    async def produce(self, student_data: dict):
        self.logger.info(f"Producing student: {student_data}")
        try:
            self.validator.validate_or_raise(student_data)
            self.logger.info("Student data validated")

            message = json.dumps(student_data).encode("utf-8")

            for attempt in range(5):
                try:
                    await self.producer.send_and_wait(self.topic, message)
                    self.logger.info(f"Successfully produced message to {self.topic}")
                    break
                except Exception as e:
                    self.logger.warning(f"Attempt {attempt + 1} failed to produce message: {e}")
                    await asyncio.sleep(1)
            else:
                self.logger.error("All attempts to produce message failed")

        except Exception as e:
            self.logger.exception(f"Validation or production failed: {e}")
class StudentService:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def get_all(self):
        self.logger.info('fetch all students!')
        with Session(engine) as session:
            students = session.exec(select(Student)).all()
            return students

class ProducerController:
    def __init__(self,
                 producer_service: ProducerService,
                 student_service: StudentService):
        self.producer_service = producer_service
        self.student_service = student_service
        self.router = APIRouter(prefix="/api/v1", tags=["Health Check"])
        self.router.post(path="/students", status_code=201, response_model=Student)(self.produce_student)
        self.router.get(path="/students", status_code=200)(self.get_all_students)
        self.logger = logging.getLogger(__name__)

    async def produce_student(self):
        self.logger.info('Producing student')
        student = generate_fake_student_dict()
        await self.producer_service.produce(student)
        return student

    def get_all_students(self):
        self.logger.info('Getting all students')
        return self.student_service.get_all()

def generate_fake_student_dict():
    return {
        "id": str(uuid.uuid4()),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email()
    }

def generate_fake_student_obj() -> Student:
    return Student.model_validate(generate_fake_student_dict())
