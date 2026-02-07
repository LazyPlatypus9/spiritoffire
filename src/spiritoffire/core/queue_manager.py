from datetime import datetime
from queue import Queue
from threading import Event
from typing import Optional

from spiritoffire.app import logger
from spiritoffire.models.queue_data import QueueData
from spiritoffire.workers.stop_item import StopItem

class QueueManager():
    _instance: Optional["QueueManager"] = None

    @classmethod
    def get_instance(cls) -> 'QueueManager':
        if cls._instance is None:
            cls._instance = QueueManager()
        return cls._instance

    def __init__(self):
        self.queue = Queue()
        self.stop = Event()

    def start(self):
        while not self.stop.is_set():
            try:
                item = self.queue.get()

                if isinstance(item, StopItem):
                    logger.info("Received StopItem, exiting loop")
                    break

                if not isinstance(item, QueueData):
                    logger.error(f"Invalid item in queue, expected {type(QueueData)}")
                    continue

                if item.retry_count > item.max_retry:
                    continue

                if datetime.now() > item.next_attempt:
                    # QueueData contains a __call__
                    item()
                else:
                    self.queue.put(item)
            except Exception as ex:
                logger.error(ex)