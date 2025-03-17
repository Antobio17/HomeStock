from datetime import datetime
from dataclasses import dataclass
from src.purchase.ticket.domain.service.dto.ticket_extractor_item_result import TicketExtractorItemResult

@dataclass
class TicketExtractorResult:
    supermarket: str
    reference: str
    subtotal: float
    discount_amount: float
    taxes: dict[str, float]
    tax_amount: float
    total: float
    purchased_at: datetime
    items: list[TicketExtractorItemResult]