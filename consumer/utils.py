import os
from sqlmodel import create_engine
from dotenv import load_dotenv
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
consumer_group=os.getenv("STUDENT_CONSUMER_GROUP")
bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS")
group_id=os.getenv("KAFKA_GROUP_ID")

DATABASE_URL = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

engine = create_engine(DATABASE_URL, echo=False)

## Kafka
consumer_config = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',  # Start from beginning if no offset
        }

## Logging
FORMAT = '%(levelname)s: %(asctime)s %(name)s - line: %(lineno)d \n\t%(message)s'
logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.DEBUG)