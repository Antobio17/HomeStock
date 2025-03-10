from typing import Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
from src.purchase.ticket.domain.model.ticket import Ticket

@dataclass
class TicketRepository(ABC):
    
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Ticket]:
        pass

    @abstractmethod
    def save(self, ticket: Ticket)  -> None:
        pass