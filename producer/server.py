from fastapi import FastAPI

from producer.producer_route import ProducerController
from producer.producer_service import ProducerService
from producer.utils import bootstrap_server, kafka_topic

app = FastAPI(title="Python Kafka API")

producer_svc = ProducerService(bootstrap_servers=bootstrap_server, topic=kafka_topic)
producer_controller = ProducerController(producer_svc)
app.include_router(producer_controller.router)