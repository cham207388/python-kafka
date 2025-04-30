import logging
import threading

from fastapi import FastAPI

from producer.producer_route import ProducerController
from producer.producer_service import ProducerService
from producer.student_service import StudentService
from producer.utils import kafka_topic
from producer.config import producer_config, student_schema_dict
from producer.grpc.grpc_server import serve_grpc

student_schema = student_schema_dict()

producer_service = ProducerService(
    config=producer_config,
    topic=kafka_topic,
    schema=student_schema
)
student_service = StudentService()
producer_controller = ProducerController(producer_service, student_service)

app = FastAPI(title="Python Kafka API")
app.include_router(producer_controller.router)

# Start gRPC server in a background thread
grpc_thread = threading.Thread(target=serve_grpc, daemon=True)
grpc_thread.start()
