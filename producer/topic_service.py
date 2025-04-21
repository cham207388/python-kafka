import logging
from confluent_kafka.admin import AdminClient, NewTopic

class TopicService:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def create_topic_if_not_exists(self, bootstrap_servers: str, topic: str):
        admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})
        topic_metadata = admin_client.list_topics(timeout=5)

        if topic in topic_metadata.topics:
            self.logger.info(f"✅ Topic '{topic}' already exists.")
            return

        # Topic config for compaction
        config = {
            "cleanup.policy": "compact"
        }

        new_topic = NewTopic(
            topic=topic,
            num_partitions=1,
            replication_factor=1,
            config=config
        )

        fs = admin_client.create_topics([new_topic])
        for topic_name, future in fs.items():
            try:
                future.result()
                self.logger.info(f"🆕 Created compacted topic: {topic_name}")
            except Exception as e:
                self.logger.error(f"❌ Failed to create topic '{topic_name}': {e}")
