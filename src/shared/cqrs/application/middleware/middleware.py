from typing import Protocol
from abc import abstractmethod

class Middleware(Protocol):
    @abstractmethod
    def before_handle(self) -> None:
        pass

    @abstractmethod
    def after_handle(self) -> None:
        pass