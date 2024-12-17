from abc import ABC, abstractmethod
from src.shared.cqrs.domain.service.dto.message import Message

class Producer(ABC):
    @abstractmethod
    def publish(self, message: Message) -> None:
        pass