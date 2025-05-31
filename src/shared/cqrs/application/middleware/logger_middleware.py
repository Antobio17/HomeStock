from dataclasses import dataclass
from src.shared.cqrs.application.middleware.middleware import Middleware
from src.shared.logger.domain.service.logger_service import LoggerService

@dataclass
class LoggerMiddleware(Middleware):
    __logger: LoggerService
    __exception: Exception 

    def before_handle(self) -> None:
        'Do nothing.'
        pass

    def after_handle(self) -> None:
        self.__logger.error(str(self.__exception))