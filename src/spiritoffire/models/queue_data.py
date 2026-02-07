from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from spiritoffire.app import logger
from spiritoffire.workers import Worker

class QueueData(BaseModel):
    worker: Worker
    retry_count: int = 0
    max_retry: int = 3
    next_attempt: datetime = datetime.now()

    def __call__(self):
        logger.info(f"Executing {__class__.__name__}, {self.retry_count} previous attempts")
        self.worker.on_start()
        self.worker.task(self.retry_count)
        self.worker.on_stop()

    model_config = ConfigDict(arbitrary_types_allowed=True)