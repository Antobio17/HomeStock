from abc import ABC, abstractmethod
from src.shared.cqrs.domain.service.dto.message import Message

class DomainEvent(Message, ABC):

    @abstractmethod
    def get_aggregate_id(self) -> dict:
        pass
