from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient

from models import Student
from utils import (
    schema_registry_url, dict_to_student, consumer_group_id, auto_offset_reset
)

schema_registry_conf = {'url': schema_registry_url}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

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