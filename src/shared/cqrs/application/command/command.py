from abc import ABC
from src.shared.cqrs.domain.service.dto.message import Message

class Command(Message, ABC):
    pass