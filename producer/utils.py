import os
import uuid
from dotenv import load_dotenv
from faker import Faker
from sqlmodel import create_engine
import logging
import sys

load_dotenv()

db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")

kafka_topic=os.getenv("KAFKA_TOPIC")
bootstrap_server=os.getenv("KAFKA_BOOTSTRAP_SERVERS")

DATABASE_URL = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
engine = create_engine(DATABASE_URL, echo=False)

fake = Faker()

def generate_fake_student():
    return {
        "id": str(uuid.uuid4()),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email()
    }

FORMAT = '%(levelname)s: %(asctime)s %(name)s - line: %(lineno)d \n\t%(message)s'
logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.DEBUG)