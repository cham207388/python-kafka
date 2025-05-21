import os
import logging
import sys
from dotenv import load_dotenv
from faker import Faker
from sqlmodel import create_engine


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

# ------------------- #
# Kafka Configuration #
# ------------------- #
kafka_topic = os.getenv("KAFKA_TOPIC")
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
acks_all = os.getenv("TOPICS_ACKS")
retries = int(os.getenv("TOPICS_RETRIES"))
linger_ms = int(os.getenv("TOPICS_LINGER_MS"))
num_of_partitions = int(os.getenv("NUM_OF_PARTITION"))
max_inflight_req_per_conn = int(os.getenv("MAX_INFLIGHT_REQUEST_PER_CONNECTION"))
retry_backoff_ms = int(os.getenv("RETRY_BACKOFF_MS"))
kafka_topic_dlt = os.getenv("KAFKA_TOPIC_DLT")
consumer_group_id = os.getenv("CONSUMER_GROUP_ID")
consumer_group_id_dlt = os.getenv("CONSUMER_GROUP_ID_DLT")
num_of_consumers=int(os.getenv("NUMBER_OF_CONSUMERS"))
auto_offset_reset = os.getenv("KAFKA_AUTO_OFFSET_RESET")

# ---------------------- #
# Fake Student Generator #
# ---------------------- #
fake = Faker()

FORMAT = '%(levelname)s: %(asctime)s %(name)s - line: %(lineno)d \n\t%(message)s'
logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.DEBUG)

# STUDENT_JSON_SCHEMA = {
#     "$schema": "https://json-schema.org/draft/2020-12/schema",
#     "$id": "https://com.abc.learning/student.schema.json",
#     "title": "Student",
#     "type": "object",
#     "properties": {
#         "id": {
#             "type": ["string", "null"]
#         },
#         "email": {
#             "type": "string",
#             "format": "email"
#         },
#         "first_name": {
#             "type": "string"
#         },
#         "last_name": {
#             "type": "string"
#         }
#     },
#     "required": ["email", "first_name", "last_name"],
#     "additionalProperties": False
# }