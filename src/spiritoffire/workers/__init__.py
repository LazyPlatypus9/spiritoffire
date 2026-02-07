from abc import abstractmethod

from pydantic import BaseModel, ConfigDict

class Worker(BaseModel):
    @abstractmethod
    def task(self, retry_count: int):
        raise NotImplementedError()
    
    @abstractmethod
    def on_start(self):
        raise NotImplementedError()

    @abstractmethod
    def on_stop(self):
        raise NotImplementedError()
    
    model_config = ConfigDict(arbitrary_types_allowed=True)