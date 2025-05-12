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

    def test_handle_message_success(self, consumer_service, mock_to_student, mock_logger):
        # Setup mock message
        mock_message = MagicMock(spec=Message)
        mock_message.key.return_value = b'test-key'
        mock_message.value.return_value = b'test-value'
        mock_message.partition.return_value = 0
        mock_message.offset.return_value = 123
        mock_message.error.return_value = None

        # Setup mock student
        mock_student = MagicMock(spec=Student)
        mock_to_student.return_value = mock_student

        # Call method
        consumer_service.handle_message(mock_message)

        # Verify calls
        mock_message.key.assert_called_once()
        mock_message.value.assert_called_once()
        mock_message.partition.assert_called_once()
        mock_message.offset.assert_called_once()
        mock_to_student.assert_called_once_with(b'test-value')
        mock_logger().info.assert_called_with(
            "Received message [key:test-key], [partition:0], [offset:123]"
        )

    def test_handle_message_failure(self, consumer_service, mock_to_student, mock_logger):
        # Setup mock message
        mock_message = MagicMock(spec=Message)
        mock_message.key.return_value = b'test-key'
        mock_message.value.return_value = b'test-value'
        mock_message.error.return_value = None

        # Simulate conversion failure
        mock_to_student.side_effect = ValueError("Invalid data")

        # Call method
        consumer_service.handle_message(mock_message)

        # Verify error was logged
        mock_logger().error.assert_called_with(
            "Failed to process message: Invalid data"
        )

    def test_persist(self, consumer_service, mock_session, mock_engine, mock_logger):
        # Setup mock student
        mock_student = MagicMock(spec=Student)

        # Create a mock session instance that will be returned by __enter__
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Call method
        consumer_service.persist(mock_student)

        # Verify session was created correctly
        mock_session.assert_called_once_with(mock_engine)

        # Verify calls on the session instance (not the class)
        mock_session_instance.add.assert_called_once_with(mock_student)
        mock_session_instance.commit.assert_called_once()

        # Verify logger call
        mock_logger().info.assert_called_with('student saved!')

    def test_consume_forever_normal_operation(self, consumer_service, mock_consumer):
        # Setup mock consumer to return:
        # 1. None (timeout)
        # 2. Valid message
        # 3. None (timeout)
        # Then raise KeyboardInterrupt to break the loop
        mock_consumer_instance = mock_consumer.return_value
        mock_consumer_instance.poll.side_effect = [
            None,
            MagicMock(error=Mock(return_value=None)),
            None,
            KeyboardInterrupt()
        ]

        # Patch handle_message to avoid testing it here
        with patch.object(consumer_service, 'handle_message') as mock_handle:
            consumer_service.consume_forever()

        # Verify consumer was closed
        mock_consumer_instance.close.assert_called_once()
    #
    def test_consume_forever_with_kafka_error(self, consumer_service, mock_consumer):
        # Setup mock consumer to return a message with error
        mock_consumer_instance = mock_consumer.return_value
        mock_error = MagicMock()
        mock_message_with_error = MagicMock(error=Mock(return_value=mock_error))
        mock_consumer_instance.poll.side_effect = [
            None,
            mock_message_with_error
        ]

        # Test that KafkaException is raised
        with pytest.raises(KafkaException):
            consumer_service.consume_forever()

        # Verify consumer was closed
        mock_consumer_instance.close.assert_called_once()
