from abc import ABC, abstractmethod

class Message(ABC):
    @abstractmethod
    def routing_key(self) -> str:
        pass