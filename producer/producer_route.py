from fastapi import APIRouter
import producer.producer_service as producer_service


class ProducerRoute:
    """
    Class-based API to handle health checks.
    """

    def __init__(self, producer: producer_service, log):
        self.producer = producer
        self.log = log
        self.router = APIRouter(prefix="/api/v1", tags=["Health Check"])
        self.router.add_api_route("/student", self.produce_student, methods=["POST"])

    def produce_student(self, student: dict):
        """
        Endpoint to check MySQL database health.
        """
        self.producer.produce(student.get("id"), student)
