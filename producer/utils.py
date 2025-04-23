import os
import uuid
import logging
import sys
from dotenv import load_dotenv
from faker import Faker
from sqlmodel import create_engine
from confluent_kafka import avro

# Database
load_dotenv()

db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=False)

## kafka
kafka_topic=os.getenv("KAFKA_TOPIC")
bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS")
acks_all=os.getenv("TOPICS_ACKS")
retries=int(os.getenv("TOPICS_RETRIES"))
linger_ms=int(os.getenv("TOPICS_LINGER_MS"))
num_of_partitions=int(os.getenv("NUM_OF_PARTITION"))
schema_registry_url=os.getenv("SCHEMA_REGISTRY_URL")
max_inflight_req_per_conn=int(os.getenv("MAX_INFLIGHT_REQUEST_PER_CONNECTION"))
retry_backoff_ms=int(os.getenv("RETRY_BACKOFF_MS"))

student_schema = avro.loads(open("./schemas/student_schema.avsc").read())
dlt_schema = avro.loads(open("./schemas/dead_letter_schema.avsc").read())
key_schema = avro.loads(open("./schemas/key_schema.avsc").read())

producer_config = {
    'bootstrap.servers': bootstrap_servers,
    'acks': acks_all,  # wait for all ISR brokers
    'enable.idempotence': True,  # ensure no duplicate delivery
    'retries': retries,  # number of automatic retries
    'retry.backoff.ms': retry_backoff_ms,  # wait 500ms between retries
    'linger.ms': linger_ms,  # allow batching for 10ms
    # 'batch.num.messages': 1000,
    # 'queue.buffering.max.messages': 10000,
    'max.in.flight.requests.per.connection': max_inflight_req_per_conn,  # keep order with idempotence
    'schema.registry.url': schema_registry_url
}

# Faker
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