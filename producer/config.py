from confluent_kafka import avro
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer

from producer.utils import (
    acks_all,
    bootstrap_servers,
    linger_ms,
    max_inflight_req_per_conn,
    retries,
    retry_backoff_ms,
    schema_registry_url,
)

student_schema_str = open("./schemas/student_schema.avsc").read()
dlt_schema = avro.loads(open("./schemas/dead_letter_schema.avsc").read())
key_schema = avro.loads(open("./schemas/key_schema.avsc").read())

schema_registry_conf = {"url": schema_registry_url}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)


avro_serializer = AvroSerializer(
    schema_registry_client=schema_registry_client,
    schema_str=student_schema_str,
    to_dict=lambda student, ctx: student.model_dump(),
)

producer_config = {
    "bootstrap.servers": bootstrap_servers,
    "acks": acks_all,
    "enable.idempotence": True,
    "retries": retries,
    "retry.backoff.ms": retry_backoff_ms,
    "linger.ms": linger_ms,
    "max.in.flight.requests.per.connection": max_inflight_req_per_conn,
    "key.serializer": StringSerializer("utf_8"),
    "value.serializer": avro_serializer,
    "partitioner": "murmur2_random",
}
