from abc import abstractmethod
from shared.cqrs.domain.service.dto.message import Message

class DomainEvent(Message):
    @abstractmethod
    def get_aggregate_id(self) -> dict:
        pass
