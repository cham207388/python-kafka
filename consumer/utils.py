import os
from sqlmodel import create_engine
from dotenv import load_dotenv

load_dotenv()

db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")

kafka_topic=os.getenv("KAFKA_TOPIC")
bootstrap_server=os.getenv("KAFKA_BOOTSTRAP_SERVER")
consumer_group=os.getenv("STUDENT_CONSUMER_GROUP")

DATABASE_URL = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

engine = create_engine(DATABASE_URL, echo=False)