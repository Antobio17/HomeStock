from typing import Optional
from dataclasses import dataclass

@dataclass
class ValidateTicketItem:
    description: str
    quantity: float
    amount: float
    product_id: str
    format_id: Optional[str] = None