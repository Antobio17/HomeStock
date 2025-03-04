from abc import ABC, abstractmethod

class Connection(ABC):
    
    @property
    @abstractmethod
    def session(self):
        pass
    
    @abstractmethod
    def close(self) -> None:
        pass