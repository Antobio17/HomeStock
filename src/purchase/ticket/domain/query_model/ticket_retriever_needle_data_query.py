from typing import Optional
from abc import ABC, abstractmethod

class TicketRetrieverNeedleDataQuery(ABC):
    
    @abstractmethod
    def get_ticket_pool(self, supermarket: str) -> Optional[str]:
        pass    