import threading

from fastapi import FastAPI

from src.config import consumer_config, producer_config, student_schema_dict
from src.consumer.main import run_consumer_instance
from src.producer.producer_route import ProducerController
from src.producer.producer_service import ProducerService
from src.producer.student_service import StudentService
from src.utils import kafka_topic, num_of_consumers

student_schema = student_schema_dict()

producer_service = ProducerService(
    config=producer_config, topic=kafka_topic, schema=student_schema
)
student_service = StudentService()
producer_controller = ProducerController(producer_service, student_service)

app = FastAPI(title="Python Kafka API")
app.include_router(producer_controller.router)

# Start consumer in the background
for i in range(num_of_consumers):
    t = threading.Thread(
        target=run_consumer_instance,
        args=(
            i,
            consumer_config,
            kafka_topic,
        ),
    )
    t.start()
