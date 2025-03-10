from typing import Optional
from dataclasses import dataclass

@dataclass
class SubmitTicketItem:
    description: str
    quantity: float
    amount: float