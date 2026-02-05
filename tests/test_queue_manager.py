from queue import Queue
from threading import Event, Thread
from unittest.mock import patch, MagicMock

import pytest

from spiritoffire.core.queue_manager import QueueManager
from spiritoffire.workers.stop_item import StopItem


class TestQueueManager:
    """Unit tests for QueueManager class."""

    def setup_method(self):
        """Reset singleton instance before each test."""
        QueueManager._instance = None

    def teardown_method(self):
        """Clean up singleton after each test."""
        QueueManager._instance = None

    def test_singleton_pattern(self):
        """Test that QueueManager follows the singleton pattern."""
        manager1 = QueueManager.get_instance()
        manager2 = QueueManager.get_instance()

        assert manager1 is manager2
        assert manager1 is manager2

    def test_init_creates_queue_and_event(self):
        """Test that __init__ initializes queue and stop event."""
        manager = QueueManager._instance = QueueManager()

        assert isinstance(manager.queue, Queue)
        assert isinstance(manager.stop, Event)

    @patch('spiritoffire.core.queue_manager.logger')
    def test_start_processes_queue_items(self, mock_logger):
        """Test that start processes items from the queue."""
        manager = QueueManager._instance = QueueManager()
        manager.stop.clear()
        manager.queue.queue.clear()

        # Add a callable item
        test_callable = MagicMock()
        manager.queue.put(test_callable)

        # Start the worker in a separate thread
        worker = Thread(target=manager.start, daemon=True)
        worker.start()
        worker.join(timeout=1)

        # Verify the callable was executed
        test_callable.assert_called_once()

    @patch('spiritoffire.core.queue_manager.logger')
    def test_start_processes_stop_item(self, mock_logger):
        """Test that start processes StopItem and exits gracefully."""
        manager = QueueManager._instance = QueueManager()
        manager.stop.clear()
        manager.queue.queue.clear()

        # Add a StopItem
        stop_item = StopItem()
        manager.queue.put(stop_item)

        # Start the worker in a separate thread
        worker = Thread(target=manager.start, daemon=True)
        worker.start()
        worker.join(timeout=1)

        # Verify logger.info was called with the expected message
        mock_logger.info.assert_called_once_with("Received StopItem, exiting loop")

    @patch('spiritoffire.core.queue_manager.logger')
    def test_start_handles_exception(self, mock_logger):
        """Test that start logs exceptions without crashing."""
        manager = QueueManager._instance = QueueManager()
        manager.stop.clear()
        manager.queue.queue.clear()

        # Add a callable that raises an exception
        test_callable = MagicMock(side_effect=Exception("Test error"))
        manager.queue.put(test_callable)

        # Start the worker in a separate thread
        worker = Thread(target=manager.start, daemon=True)
        worker.start()
        worker.join(timeout=1)

        # Verify logger.error was called with the exception
        mock_logger.error.assert_called_once()

    @patch('spiritoffire.core.queue_manager.logger')
    def test_start_continues_after_error(self, mock_logger):
        """Test that start continues processing after an exception."""
        manager = QueueManager._instance = QueueManager()
        manager.stop.clear()
        manager.queue.queue.clear()

        # Add both an error-causing item and a valid item
        test_callable_error = MagicMock(side_effect=Exception("Error"))
        test_callable_success = MagicMock()
        manager.queue.put(test_callable_error)
        manager.queue.put(test_callable_success)

        # Start the worker in a separate thread
        worker = Thread(target=manager.start, daemon=True)
        worker.start()
        worker.join(timeout=1)

        # Verify both callables were attempted
        test_callable_error.assert_called_once()
        test_callable_success.assert_called_once()

    @patch('spiritoffire.core.queue_manager.logger')
    def test_start_skips_none_item(self, mock_logger):
        """Test that start skips None items in the queue."""
        manager = QueueManager._instance = QueueManager()
        manager.stop.clear()
        manager.queue.queue.clear()

        # Add a None item
        manager.queue.put(None)
        manager.queue.put(StopItem())

        # Start the worker in a separate thread
        worker = Thread(target=manager.start, daemon=True)
        worker.start()
        worker.join(timeout=1)

        # StopItem should have been processed and stopped the loop
        mock_logger.info.assert_called_once_with("Received StopItem, exiting loop")