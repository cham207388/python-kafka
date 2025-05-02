from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import StringSerializer

from src.models import Student
from src.utils import (
    schema_registry_url,
    consumer_group_id,
    auto_offset_reset,
    bootstrap_servers,
    acks_all, retries,
    retry_backoff_ms,
    linger_ms,
    max_inflight_req_per_conn,
    student_schema_str
)

schema_registry_conf = {'url': schema_registry_url}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

## Producer
avro_serializer = AvroSerializer(
    schema_registry_client=schema_registry_client,
    schema_str=student_schema_str,
    to_dict=lambda student, ctx: student.model_dump()
)

producer_config = {
    'bootstrap.servers': bootstrap_servers,
    'acks': acks_all,
    'enable.idempotence': True,
    'retries': retries,
    'retry.backoff.ms': retry_backoff_ms,
    'linger.ms': linger_ms,
    'max.in.flight.requests.per.connection': max_inflight_req_per_conn,
    'key.serializer': StringSerializer('utf_8'),
    'value.serializer': avro_serializer,
    'partitioner': 'murmur2_random'
}

## Consumer
avro_deserializer = AvroDeserializer(
    schema_registry_client=schema_registry_client,
    schema_str=open("./schemas/student_schema.avsc").read(),
    from_dict=lambda data, ctx: Student.model_validate(data)
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
