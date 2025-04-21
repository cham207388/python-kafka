# from producer_service import ProducerService
# from producer.utils import generate_fake_student
import uuid

# kafka_producer = ProducerService(bootstrap_servers="localhost:9092", topic="student")

# student_data = generate_fake_student()

# kafka_producer.send(key=str(student_data["id"]), value=student_data)
# kafka_producer.flush()


try:
    # Convert UUID string to int for partitioning
    uuid_str = uuid.uuid4()
    print(f'uuid is: {uuid_str}')
    int_key = uuid_str.int
    print(f'int uuid is: {int_key}')
    partition_key = str(int_key % 2)
    print(f'partition_key is: {partition_key}')
except (ValueError, AttributeError):
    print(f"⚠️ Key is not a valid UUID. Defaulting to partition key '0'")
    partition_key = '0'