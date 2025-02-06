from datetime import datetime
from dataclasses import dataclass

@dataclass
class User:
    id: str
    email: str
    sub: str
    created_at: datetime