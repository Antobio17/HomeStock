from dataclasses import dataclass
from src.shared.cqrs.application.command.command import Command
from src.purchase.ticket.application.command.dto.finish_ticket_validation_item import FinishTicketValidationItem

@dataclass
class FinishTicketValidationCommand(Command):
    ticket_id: str
    items: list[FinishTicketValidationItem]
    
    @staticmethod
    def get_name() -> str:
        return 'homestock.purchase.1.command.ticket.finish_validation'