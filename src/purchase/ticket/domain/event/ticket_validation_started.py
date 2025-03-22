from datetime import datetime
from dataclasses import dataclass
from src.shared.cqrs.domain.event.domain_event import DomainEvent

@dataclass
class TicketValidationStarted(DomainEvent):
    aggregate_id: str
    reference: str
    status: str
    items: list[dict]
    subtotal: float
    discount_amount: float
    taxes: dict[str, float]
    tax_amount: float
    total: float
    purchased_at: datetime
    updated_at: datetime
    
    def get_aggregate_id(self) -> str:
        return self.aggregate_id
    
    @staticmethod
    def get_name() -> str:
        return 'homestock.purchase.1.event.ticket.validation_started'