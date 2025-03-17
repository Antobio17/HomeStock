from abc import ABC, abstractmethod

class TicketRetrieverService(ABC):
    
    @abstractmethod
    def execute(self) -> list[str]:
        pass