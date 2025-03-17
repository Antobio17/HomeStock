from dataclasses import dataclass

@dataclass
class TicketExtractorItemResult:
    description: str
    quantity: float
    amount: float