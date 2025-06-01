from dataclasses import dataclass
from src.shared.database.domain.connection.connection import Connection
from src.shared.cqrs.application.middleware.middleware import Middleware

@dataclass
class DatabaseConnectionMiddleware(Middleware):
    __connection: Connection

    def before_handle(self) -> None:
        'Do nothing.'
        pass

    def after_handle(self) -> None:
        if self.__connection is None:
            return
        
        self.__connection.close()