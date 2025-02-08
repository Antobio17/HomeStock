from abc import ABC, abstractmethod

class Connection(ABC):
    
    @property
    @abstractmethod
    def session(self) -> object:
        pass
    
    @abstractmethod
    def close(self) -> None:
        pass