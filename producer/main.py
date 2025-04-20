from producer_service import ProducerService
from env_vars import generate_fake_student

if __name__ == "__main__":
    kafka_producer = ProducerService(bootstrap_servers="localhost:9092", topic="student")

    student_data = generate_fake_student()

    kafka_producer.produce(key=str(student_data["id"]), value=student_data)
    kafka_producer.flush()