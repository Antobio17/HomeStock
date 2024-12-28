from abc import ABC, abstractmethod

class Message(ABC):
    
    @staticmethod
    @abstractmethod
    def get_name() -> str:
        pass