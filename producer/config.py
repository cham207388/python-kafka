from confluent_kafka import avro
import json

from producer.utils import (
    bootstrap_servers,
    acks_all,
    retries,
    retry_backoff_ms,
    linger_ms,
    max_inflight_req_per_conn
)

def student_schema_dict():
    with open('./schemas/student_schema.avsc') as f:
        return json.load(f)

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