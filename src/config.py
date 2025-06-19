import json

from src.utils import (
    acks_all,
    auto_offset_reset,
    bootstrap_servers,
    consumer_group_id,
    linger_ms,
    max_inflight_req_per_conn,
    retries,
    retry_backoff_ms,
)


def student_schema_dict():
    with open("./schemas/student_schema.avsc") as f:
        return json.load(f)


producer_config = {
    "bootstrap.servers": bootstrap_servers,
    "acks": acks_all,
    "enable.idempotence": True,
    "retries": retries,
    "retry.backoff.ms": retry_backoff_ms,
    "linger.ms": linger_ms,
    "max.in.flight.requests.per.connection": max_inflight_req_per_conn,
    "partitioner": "murmur2_random",
}

consumer_config = {
    "bootstrap.servers": bootstrap_servers,
    "group.id": consumer_group_id,
    "enable.auto.commit": False,  # 🔒 You commit only when you're ready
    "enable.auto.offset.store": False,  # 🔧 Manual control over offset storage
    "auto.offset.reset": auto_offset_reset,  # 📜 Start from beginning if no prior commit
    "session.timeout.ms": 15_000,  # 💓 Heartbeat timeout (15s)
    "heartbeat.interval.ms": 5_000,  # 💓 Heartbeat every 5s
}
