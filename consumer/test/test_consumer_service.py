import pytest
from unittest.mock import Mock, patch, call, MagicMock
from confluent_kafka import KafkaException, Message
from sqlmodel import Session
import logging
from consumer.models import Student  # assuming this exists based on to_student
from consumer.consumer_service import ConsumerService


# Test implementation
class TestConsumerService:
    @pytest.fixture
    def mock_consumer(self):
        with patch('consumer.consumer_service.Consumer') as mock:
            yield mock
#
    @pytest.fixture
    def mock_session(self):
        with patch('consumer.consumer_service.Session') as mock:
            yield mock

    @pytest.fixture
    def mock_engine(self):
        with patch('consumer.consumer_service.engine') as mock:
            yield mock

    @pytest.fixture
    def mock_to_student(self):
        with patch('consumer.consumer_service.to_student') as mock:
            yield mock

    @pytest.fixture
    def mock_logger(self):
        with patch('consumer.consumer_service.logging.getLogger') as mock:
            yield mock

    @pytest.fixture
    def consumer_service(self, mock_consumer, mock_logger):
        config = {'bootstrap.servers': 'localhost:9092', 'group.id': 'test-group'}
        topic = 'test-topic'
        return ConsumerService(topic, config)

    def test_initialization(self, consumer_service, mock_consumer, mock_logger):
        mock_consumer.assert_called_once()
        mock_logger().info.assert_called_once_with(f"📡 Subscribed to topic: test-topic")

