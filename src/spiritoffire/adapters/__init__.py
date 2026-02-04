from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Generator

T = TypeVar("T")

class DatabaseAdapter(ABC, Generic[T]):
    @abstractmethod
    def add(self, item: T) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self) -> Generator[T, None, None]:
        raise NotImplementedError