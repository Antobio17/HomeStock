from dataclasses import dataclass

@dataclass
class FinishTicketValidationItem:
    ticket_item_id: str
    format_id: str