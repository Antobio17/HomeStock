from datetime import datetime
from dataclasses import dataclass
from src.shared.cqrs.application.command.command import Command
from src.purchase.ticket.application.command.dto.submit_ticket_item import SubmitTicketItem

@dataclass
class SubmitTicketCommand(Command):
    supermarket: str
    reference: str
    subtotal: float
    discount_amount: float
    taxes: dict[str, float]
    tax_amount: float
    total: float
    purchased_at: datetime
    items: list[SubmitTicketItem]