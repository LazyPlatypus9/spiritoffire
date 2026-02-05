from queue import Queue
from threading import Event
from typing import Optional

from spiritoffire.app import logger
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

                if item:
                    # QueueData contains a __call__
                    item()
            except Exception as ex:
                logger.error(ex)