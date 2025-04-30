import grpc
from concurrent import futures
import logging

from producer.grpc import student_pb2_grpc, student_pb2
from producer.producer_service import ProducerService
from producer.models import Student
from producer.utils import kafka_topic, num_of_partitions
from producer.config import producer_config, student_schema_dict


class GRPCStudentService(student_pb2_grpc.StudentServiceServicer):
    def __init__(self, producer_service: ProducerService):
        self.producer_service = producer_service
        self.logger = logging.getLogger(__name__)

    def SubmitStudent(self, request, context):
        try:
            student = Student(
                id=request.id,
                email=request.email,
                first_name=request.first_name,
                last_name=request.last_name
            )
            partition = self.producer_service.get_partition(student.id, num_of_partitions)
            self.producer_service.send(key=student.id, value=student, partition=partition)
            return student_pb2.SubmitResponse(status="SUCCESS", message="Student submitted to Kafka")
        except Exception as e:
            self.logger.exception("gRPC SubmitStudent failed")
            return student_pb2.SubmitResponse(status="FAILURE", message=str(e))


def serve_grpc():
    student_schema = student_schema_dict()
    producer_service = ProducerService(
        config=producer_config,
        topic=kafka_topic,
        schema=student_schema
    )
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_pb2_grpc.add_StudentServiceServicer_to_server(
        GRPCStudentService(producer_service),
        server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("🚀 gRPC server running at port 50051")
    server.wait_for_termination()