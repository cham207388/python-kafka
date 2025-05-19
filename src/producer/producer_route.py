import logging
from fastapi import APIRouter

from src.models import Student
from src.producer.producer_service import ProducerService
from src.producer.student_service import StudentService
from src.utils import generate_fake_student_dict


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

    def produce_student(self):
        self.logger.info('Producing student')
        student = generate_fake_student_dict()
        self.producer_service.produce(student)
        return student

    def get_all_students(self):
        self.logger.info('Getting all students')
        return self.student_service.get_all()
