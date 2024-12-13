from typing import Protocol
from abc import abstractmethod
from src.shared.cqrs.application.command.command import Command

class Middleware(Protocol):
    @abstractmethod
    def before_handle(self) -> None:
        pass

    @abstractmethod
    def after_handle(self) -> None:
        pass