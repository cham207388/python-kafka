import io
import logging
import mmh3
from confluent_kafka import Producer
from fastavro import schemaless_writer, parse_schema, validate

from producer.models import Student
from producer.producer_callback import ProducerCallback


class ProducerService:
    def __init__(self, config: dict, topic: str, schema: dict):
        self.config = config
        self.topic = topic
        self.schema = parse_schema(schema)
        self.producer = Producer(self.config)
        self.logger = logging.getLogger(__name__)

    def _serialize_avro(self, record: dict) -> bytes:
        """Manually serialize a record to Avro bytes."""
        # Validate against the schema
        if not validate(record, self.schema):
            raise ValueError(f"Record does not conform to Avro schema: {record}")
        bytes_writer = io.BytesIO()
        schemaless_writer(bytes_writer, self.schema, record)
        return bytes_writer.getvalue()

    def send(self, key: str, value: Student, partition: int):
        try:
            self.logger.info(f"Producing record:{value} to topic: {self.topic}")
            serialized_value = self._serialize_avro(value.model_dump())
            self.producer.produce(
                topic=self.topic,
                key=key,
                value=serialized_value,
                partition=partition,
                on_delivery=ProducerCallback(value)
            )
            self.producer.flush()
        except ValueError as e:
            self.logger.error(f"🛑 Schema validation error: {e}")
        except BufferError as e:
            self.logger.error(f"❗ Local producer queue is full ({len(self.producer)} messages awaiting delivery): {e}")
        except Exception as e:
            self.logger.exception("Unexpected error while producing message")
        
    def get_partition(self, key: str, num_partitions: int):
        key_bytes = key.encode("utf-8")
        hash_value = mmh3.hash(key_bytes, signed=False)
        return hash_value % num_partitions
