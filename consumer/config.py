from utils import consumer_group_id, auto_offset_reset

import json

def student_schema_dict():
    with open('./schemas/student_schema.avsc') as f:
        return json.load(f)

student_schema_str = open("./schemas/student_schema.avsc").read()


consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": consumer_group_id,
    "enable.auto.commit": False,  # 🔒 You commit only when you're ready
    "enable.auto.offset.store": False,  # 🔧 Manual control over offset storage
    "auto.offset.reset": auto_offset_reset,  # 📜 Start from beginning if no prior commit
    "session.timeout.ms": 15_000,  # 💓 Heartbeat timeout (15s)
    "heartbeat.interval.ms": 5_000  # 💓 Heartbeat every 5s
}