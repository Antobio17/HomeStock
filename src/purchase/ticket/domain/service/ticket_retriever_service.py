from typing import Optional
from abc import ABC, abstractmethod

class TicketRetrieverService(ABC):
    
    @abstractmethod
    def execute(self) -> Optional[str]:
        pass