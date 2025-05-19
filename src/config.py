from src.utils import (
    consumer_group_id,
    auto_offset_reset,
    bootstrap_servers,
    acks_all, retries,
    retry_backoff_ms,
    linger_ms,
    max_inflight_req_per_conn
)

## Producer
STUDENT_JSON_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://com.abc.learning/student.schema.json",
    "title": "Student",
    "type": "object",
    "properties": {
        "id": {
            "type": ["string", "null"]
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "first_name": {
            "type": "string"
        },
        "last_name": {
            "type": "string"
        }
    },
    "required": ["email", "first_name", "last_name"],
    "additionalProperties": False
}

producer_config = {
    'bootstrap.servers': bootstrap_servers,
    'acks': acks_all,
    'enable.idempotence': True,
    'retries': retries,
    'retry.backoff.ms': retry_backoff_ms,
    'linger.ms': linger_ms,
    'max.in.flight.requests.per.connection': max_inflight_req_per_conn,
    'partitioner': 'murmur2_random'
}

## Consumer

consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": consumer_group_id,
    "enable.auto.commit": False,  # 🔒 You commit only when you're ready
    "enable.auto.offset.store": False,  # 🔧 Manual control over offset storage
    "auto.offset.reset": auto_offset_reset,  # 📜 Start from beginning if no prior commit
    "session.timeout.ms": 15_000,  # 💓 Heartbeat timeout (15s)
    "heartbeat.interval.ms": 5_000,  # 💓 Heartbeat every 5s
}
