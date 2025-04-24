import logging
import uuid
from fastapi import APIRouter

from producer.models import Student
from producer.producer_service import ProducerService
from producer.student_service import StudentService
from producer.utils import generate_fake_student_dict, num_of_partitions, generate_fake_student_obj


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
        student = generate_fake_student_obj()
        key = student.id
        partition = self.producer_service.get_partition(key, num_partitions=num_of_partitions)
        self.producer_service.send(key=key, value=student, partition=partition)
        return student

    def get_all_students(self):
        self.logger.info('Getting all students')
        return self.student_service.get_all()
