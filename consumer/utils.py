import logging
import os
import sys

from dotenv import load_dotenv
from sqlmodel import create_engine

load_dotenv()


def dict_to_student(obj, ctx):
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

FORMAT = "%(levelname)s: %(asctime)s %(name)s - line: %(lineno)d \n\t%(message)s"
logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.DEBUG)
