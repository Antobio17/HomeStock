from datetime import datetime
from dataclasses import dataclass
from src.purchase.ticket.application.command.dto.submit_ticket_item import SubmitTicketItem

@dataclass
class SubmitTicketCommand:
    supermarket: str
    reference: str
    subtotal: float
    discount_amount: float
    taxes: dict[str, float]
    tax_amount: float
    total: float
    purchased_at: datetime
    items: list[SubmitTicketItem]