import os
import uuid
import logging
import sys
from dotenv import load_dotenv
from faker import Faker
from sqlmodel import create_engine

# database
load_dotenv()

db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")

DATABASE_URL = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
engine = create_engine(DATABASE_URL, echo=False)

# kafka
kafka_topic=os.getenv("KAFKA_TOPIC")
bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVER")
acks_all=os.getenv("TOPICS_STUDENT_ADV_ACK")
retries=int(os.getenv("TOPICS_STUDENT_ADV_RETRIES"))
linger_ms=int(os.getenv("TOPICS_STUDENT_ADV_LINGER_MS"))
num_of_partitions=int(os.getenv("NUM_OF_PARTITION"))

producer_config = {
  'bootstrap.servers': bootstrap_servers,
  'acks': acks_all,  # wait for all ISR brokers
  'enable.idempotence': True,  # ensure no duplicate delivery
  'retries': retries,  # number of automatic retries
  'retry.backoff.ms': 500,  # wait 500ms between retries
  'linger.ms': linger_ms,  # allow batching for 10ms
  # 'batch.num.messages': 1000,
  # 'queue.buffering.max.messages': 10000,
  'max.in.flight.requests.per.connection': 5  # keep order with idempotence
}

# faker
fake = Faker()

def generate_fake_student():
    return {
        "id": str(uuid.uuid4()),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email()
    }

# logger
FORMAT = '%(levelname)s: %(asctime)s %(name)s - line: %(lineno)d \n\t%(message)s'
logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.DEBUG)