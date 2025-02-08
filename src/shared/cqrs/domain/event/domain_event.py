from abc import ABC, abstractmethod

class DomainEvent(ABC):
    @abstractmethod
    def get_aggregate_id(self) -> dict:
        pass
