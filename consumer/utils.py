import os
import logging
import sys
from sqlmodel import create_engine
from dotenv import load_dotenv

from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient

load_dotenv()


def student_from_dict(obj, ctx):
    return obj  # Or construct a Pydantic/SQLModel if needed


# database
db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=False)

# kafka
kafka_topic = os.getenv("KAFKA_TOPIC")
kafka_topic_dlt = os.getenv("KAFKA_TOPIC_DLT")
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
consumer_group_id = os.getenv("CONSUMER_GROUP_ID")
auto_offset_reset = os.getenv("KAFKA_AUTO_OFFSET_RESET")
schema_registry_url = os.getenv("SCHEMA_REGISTRY_URL")

schema_registry_conf = {'url': schema_registry_url}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

avro_deserializer = AvroDeserializer(
    schema_registry_client=schema_registry_client,
    schema_str=open("./schemas/student_schema.avsc").read(),
    from_dict=student_from_dict
)

consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": consumer_group_id,
    "enable.auto.commit": False,  # 🔒 You commit only when you're ready
    "enable.auto.offset.store": False,  # 🔧 Manual control over offset storage
    "auto.offset.reset": auto_offset_reset,  # 📜 Start from beginning if no prior commit
    "session.timeout.ms": 15_000,  # 💓 Heartbeat timeout (15s)
    "heartbeat.interval.ms": 5_000,  # 💓 Heartbeat every 5s
    'key.deserializer': StringDeserializer('utf_8'),
    'value.deserializer': avro_deserializer
}

FORMAT = '%(levelname)s: %(asctime)s %(name)s - line: %(lineno)d \n\t%(message)s'
logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.DEBUG)
