from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Generator, Optional

T = TypeVar("T")

class DatabaseAdapter(ABC, Generic[T]):
    @abstractmethod
    def add(self, item: T) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self) -> Generator[T, None, None]:
        raise NotImplementedError
    
    @abstractmethod
    def exists(self, item: T) -> Optional[T]:
        raise NotImplementedError