from abc import ABC, abstractmethod
from src.shared.cqrs.domain.event.domain_event import DomainEvent

class Subscriber(ABC):
    
    @abstractmethod
    def handle(self, event: DomainEvent) -> None:
        pass