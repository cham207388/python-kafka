from fastapi import FastAPI

from .producer_route import ProducerController
from .producer_service import ProducerService


app = FastAPI(title="Python Kafka API")

producer_svc = ProducerService(bootstrap_servers="localhost:9092", topic="student")
producer_controller = ProducerController(producer_svc)
app.include_router(producer_controller.router)