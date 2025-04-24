import os
import uuid
import logging
import sys
from dotenv import load_dotenv
from faker import Faker
from sqlmodel import create_engine
from confluent_kafka import avro

from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import StringSerializer

# ---------------------- #
# Database Configuration #
# ---------------------- #
load_dotenv()

db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=False)

# ------------------ #
# Kafka Configuration #
# ------------------ #
kafka_topic = os.getenv("KAFKA_TOPIC")
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
acks_all = os.getenv("TOPICS_ACKS")
retries = int(os.getenv("TOPICS_RETRIES"))
linger_ms = int(os.getenv("TOPICS_LINGER_MS"))
num_of_partitions = int(os.getenv("NUM_OF_PARTITION"))
schema_registry_url = os.getenv("SCHEMA_REGISTRY_URL")
max_inflight_req_per_conn = int(os.getenv("MAX_INFLIGHT_REQUEST_PER_CONNECTION"))
retry_backoff_ms = int(os.getenv("RETRY_BACKOFF_MS"))

student_schema_str = open("./schemas/student_schema.avsc").read()
dlt_schema = avro.loads(open("./schemas/dead_letter_schema.avsc").read())
key_schema = avro.loads(open("./schemas/key_schema.avsc").read())

schema_registry_conf = {'url': schema_registry_url}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# ✅ FIXED: Proper to_dict function
def student_to_dict(obj, ctx):
    return obj  # dict already

avro_serializer = AvroSerializer(
    schema_registry_client=schema_registry_client,
    schema_str=student_schema_str,
    to_dict=student_to_dict
)

producer_config = {
    'bootstrap.servers': bootstrap_servers,
    'acks': acks_all,
    'enable.idempotence': True,
    'retries': retries,
    'retry.backoff.ms': retry_backoff_ms,
    'linger.ms': linger_ms,
    'max.in.flight.requests.per.connection': max_inflight_req_per_conn,
    'key.serializer': StringSerializer('utf_8'),
    'value.serializer': avro_serializer
}

# ------------------ #
# Fake Student Generator #
# ------------------ #
fake = Faker()

def generate_fake_student():
    return {
        "id": str(uuid.uuid4()),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email()
    }

# Logger setup
FORMAT = '%(levelname)s: %(asctime)s %(name)s - line: %(lineno)d \n\t%(message)s'
logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.DEBUG)