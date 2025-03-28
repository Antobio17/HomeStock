from datetime import datetime
from dataclasses import dataclass
from src.shared.cqrs.application.command.command import Command
from src.purchase.ticket.application.command.dto.start_ticket_validation_item import StartTicketValidationItem

@dataclass
class StartTicketValidationCommand(Command):
    ticket_id: str
    reference: str
    subtotal: float
    discount_amount: float
    taxes: dict[str, float]
    tax_amount: float
    total: float
    purchased_at: datetime
    items: list[StartTicketValidationItem]
    
    @staticmethod
    def get_name() -> str:
        return 'homestock.purchase.1.command.ticket.validate'