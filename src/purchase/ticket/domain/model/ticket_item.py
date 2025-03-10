import uuid
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
from src.shared.cqrs.domain.event.domain_event import DomainEvent

@dataclass
class TicketItem:
    id: str
    ticket_id: str
    description: str
    quantity: float
    unit_price: float
    amount: float
    format_id: Optional[str] = None
    product_id: Optional[str] = None