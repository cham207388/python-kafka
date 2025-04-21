import uuid
from fastapi import APIRouter
from producer.producer_service import ProducerService
from producer.models import StudentRequest

class ProducerController:
    """
    Class-based API to handle health checks.
    """

    def __init__(self, producer: ProducerService):
        self.producer = producer
        self.router = APIRouter(prefix="/api/v1", tags=["Health Check"])
        self.router.add_api_route("/student", self.produce_student, methods=["POST"])

    def produce_student(self, student: StudentRequest):
        """
        Endpoint to check MySQL database health.
        """
        student.id = str(uuid.uuid4())
        self.producer.send(student.id, student.model_dump())
