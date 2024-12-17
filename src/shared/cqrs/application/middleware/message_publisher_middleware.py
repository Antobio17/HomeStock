from dataclasses import dataclass
from src.shared.cqrs.application.command.command import Command
from src.shared.cqrs.application.middleware.middleware import Middleware
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher

@dataclass
class MessagePuclisherMiddleware(Middleware):
    __message_publisher: MessagePublisher

    def before_handle(self) -> None:
        self.__message_publisher.disable_publish_instantly()

    def after_handle(self) -> None:
        self.__message_publisher.execute_messages()