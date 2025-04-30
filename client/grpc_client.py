import sys
from pathlib import Path

# Add project root to PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parents[1]))

import grpc
import uuid
from faker import Faker

from producer.grpc.student_pb2_grpc import StudentServiceStub
from producer.grpc.student_pb2 import Student  # ✅ Import protobuf message class

fake = Faker()

def create_test_student():
    return Student(
        id=str(uuid.uuid4()),
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name()
    )

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = StudentServiceStub(channel)

    student = create_test_student()
    print(f"🎓 Sending student: {student}")

    response = stub.SubmitStudent(student)
    print(f"✅ Response: status={response.status}, message='{response.message}'")

if __name__ == "__main__":
    run()