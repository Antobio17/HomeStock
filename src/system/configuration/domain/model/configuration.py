from datetime import datetime
from dataclasses import dataclass

TICKET_POOL = 'ticket_pool'

@dataclass
class Configuration:
    id: str
    code: str
    payload: dict
    created_at: datetime
    updated_at: datetime