from abc import ABC, abstractmethod

class DomainEvent(ABC):
    @abstractmethod
    def event_name(self) -> str:
        pass
    
    @abstractmethod
    def aggregate_id(self) -> dict:
        pass