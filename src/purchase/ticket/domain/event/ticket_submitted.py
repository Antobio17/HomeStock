from datetime import datetime
from dataclasses import dataclass
from src.shared.cqrs.domain.event.domain_event import DomainEvent

@dataclass
class TicketSubmitted(DomainEvent):
    aggregate_id: str
    supermarket: str
    reference: str
    status: str
    items: list[dict]
    subtotal: float
    discount_amount: float
    taxes: dict[float, float]
    tax_amount: float
    total: float
    purchased_at: datetime
    created_at: datetime
    
    def get_aggregate_id(self) -> str:
        return self.aggregate_id
    
    @staticmethod
    def get_name() -> str:
        return 'homestock.purchase.1.event.ticket.submitted'