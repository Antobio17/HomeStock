from src.shared.cqrs.domain.service.dto.message import Message

class MessagePublisher():
    def execute(self, message: Message) -> None:
        pass