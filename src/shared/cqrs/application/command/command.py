from abc import ABC
from shared.cqrs.domain.service.dto.message import Message

class Command(Message, ABC):
    pass