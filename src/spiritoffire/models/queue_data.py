from pydantic import BaseModel, ConfigDict

from spiritoffire.app import logger
from spiritoffire.workers import Worker

class QueueData(BaseModel):
    worker: Worker

    def __call__(self):
        logger.info("Executing {__class__.__name__}")
        self.worker.on_start()
        self.worker.task()
        self.worker.on_stop()

    model_config = ConfigDict(arbitrary_types_allowed=True)