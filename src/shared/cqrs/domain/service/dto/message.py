from abc import ABC, abstractmethod

class Message(ABC):
    
    @property
    @abstractmethod
    def routing_key(self) -> str:
        pass