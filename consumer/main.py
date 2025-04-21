from consumer_service import ConsumerService
from utils import bootstrap_server, kafka_topic, consumer_group

consumer = ConsumerService(
  bootstrap_servers=bootstrap_server,
  topic=kafka_topic,
  group_id=consumer_group
)
consumer.consume_forever()