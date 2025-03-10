from typing import Optional
from dataclasses import dataclass
from src.purchase.ticket.domain.model.ticket import Ticket
from src.purchase.ticket.domain.model.ticket_repository import TicketRepository

@dataclass
class InMemoryTickeyRepository(TicketRepository):
    __ticket: Optional[Ticket] = None
    __saved: Optional[Ticket] = None
    
    def find_by_id(self, id: str) -> Optional[Ticket]:
        if self.__ticket is None or self.__ticket.id != id:
            return None
        return self.__ticket

    def save(self, ticket: Ticket) -> None:
        self.__saved = ticket
        
    def spy(self) -> Optional[Ticket]:
        return self.__saved
    
    def will_return(self, ticket: Ticket) -> None:
        self.__ticket = ticket
