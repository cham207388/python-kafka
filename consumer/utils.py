import os
import logging
import sys
from sqlmodel import create_engine
from dotenv import load_dotenv

load_dotenv()

# database
db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=False)

# kafka
kafka_topic=os.getenv("KAFKA_TOPIC")
kafka_topic_dlt=os.getenv("KAFKA_TOPIC_DLT")
bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS")
consumer_group_id=os.getenv("CONSUMER_GROUP_ID")
auto_offset_reset=os.getenv("KAFKA_AUTO_OFFSET_RESET")


# consumer_config = {
#     'bootstrap.servers': bootstrap_servers,
#     'group.id': consumer_group_id,
#     'auto.offset.reset': auto_offset_reset,  # Start from beginning if no offset
# }

consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": consumer_group_id,
    "enable.auto.commit": False,                  # 🔒 You commit only when you're ready
    "enable.auto.offset.store": False,            # 🔧 Manual control over offset storage
    "auto.offset.reset": auto_offset_reset,       # 📜 Start from beginning if no prior commit
    "session.timeout.ms": 15_000,                 # 💓 Heartbeat timeout (15s)
    "heartbeat.interval.ms": 5_000,               # 💓 Heartbeat every 5s
    # "max.poll.interval.ms": 300_000,              # ⏱️ Max time (5min) before Kafka revokes partition
    # "fetch.min.bytes": 1_000,                     # 🧠 Wait until there's enough data
    # "fetch.max.bytes": 5_242_880,                 # 5MB max fetch
    # "queued.min.messages": 1000,                  # 🛒 Min queued messages
    # "queued.max.messages.kbytes": 10240,          # 🛒 Max 10MB in buffer
    # "client.id": "student-consumer-1",            # 👤 Helpful for monitoring
    # "debug": "cgrp,topic,fetch"                   # 🛠️ Optional: enable for verbose logs
}

FORMAT = '%(levelname)s: %(asctime)s %(name)s - line: %(lineno)d \n\t%(message)s'
logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.DEBUG)
