from dataclasses import dataclass
from src.shared.cqrs.domain.service.dto.metadata import Metadata
from src.shared.cqrs.application.middleware.middleware import Middleware
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher

@dataclass
class MessagePublisherMiddleware(Middleware):
    __message_publisher: MessagePublisher
    __metadata: Metadata

    def before_handle(self) -> None:
        self.__message_publisher.disable_publish_instantly()

    def after_handle(self) -> None:
        self.__message_publisher.flush(self.__metadata)