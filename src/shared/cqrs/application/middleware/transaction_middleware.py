from dataclasses import dataclass, field
from src.shared.cqrs.application.command.command import Command
from src.shared.cqrs.application.middleware.middleware import Middleware
from src.shared.database.domain.manager.transaction_manager import TransactionManager

@dataclass
class TransactionMiddleware(Middleware):
    __transaction_mediator: TransactionManager = field(default_factory=TransactionManager) 

    def before_handle(self) -> None:
        self.__transaction_mediator.begin()

    def after_handle(self) -> None:
        self.__transaction_mediator.commit()