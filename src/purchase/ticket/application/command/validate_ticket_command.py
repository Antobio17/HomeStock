from datetime import datetime
from dataclasses import dataclass
from src.shared.cqrs.application.command.command import Command
from src.purchase.ticket.application.command.dto.validate_ticket_item import ValidateTicketItem

@dataclass
class ValidateTicketCommand(Command):
    ticket_id: str
    reference: str
    subtotal: float
    discount_amount: float
    taxes: dict[str, float]
    tax_amount: float
    total: float
    purchased_at: datetime
    items: list[ValidateTicketItem]
    
    @staticmethod
    def get_name() -> str:
        return 'homestock.purchase.1.command.ticket.validate'