from abc import ABC, abstractmethod

class TransactionManager(ABC):
    
    @property
    @abstractmethod
    def session(self) -> object:
        pass

    @abstractmethod
    def begin(self) -> None:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass