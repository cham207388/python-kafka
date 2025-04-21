import logging
import uuid
from fastapi import APIRouter
from producer.producer_service import ProducerService
from producer.models import StudentRequest
from producer.student_service import StudentService

class ProducerController:
    def __init__(self, 
                 producer_service: ProducerService, 
                 student_service: StudentService):
        self.producer_service = producer_service
        self.student_service = student_service
        self.router = APIRouter(prefix="/api/v1", tags=["Health Check"])
        self.router.post("/students")(self.produce_student)
        self.router.get("/students")(self.get_all_students)
        self.logger = logging.getLogger(__name__)

    def produce_student(self, student: StudentRequest):
        """
        Endpoint to check MySQL database health.
        """
        student.id = str(uuid.uuid4())
        self.producer_service.send(student.id, student.model_dump())
        
    def get_all_students(self):
        self.logger.info('Getting all students')
        return self.student_service.get_all()
