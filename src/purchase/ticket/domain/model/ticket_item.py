from typing import Optional
from dataclasses import dataclass
from src.shared.cqrs.domain.event.domain_event import DomainEvent

@dataclass
class TicketItem:
    id: str
    ticket_id: str
    description: str
    quantity: float
    unit_price: float
    amount: float
    product_id: Optional[str] = None
    format_id: Optional[str] = None
    
    def assign_format_id(self, format_id: str) -> None:
        self.format_id =  format_id