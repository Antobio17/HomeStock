from typing import Optional
from abc import ABC, abstractmethod

class ValidateTicketNeedleDataQuery(ABC):
    
    @abstractmethod
    def formats(self, format_names: list[str]) -> Optional[dict]:
        pass
    
    @abstractmethod
    def items(self, ticket_id: str) -> list[dict]:
        pass