from datetime import datetime
from dataclasses import dataclass
from src.shared.cqrs.domain.service.dto.message import Message
from src.shared.cqrs.domain.event.domain_event import DomainEvent

@dataclass
class FormatCreated(DomainEvent, Message):
    aggregate_id: str
    product_id: str
    name: str
    created_at: datetime
    enabled_at: datetime
    
    def get_aggregate_id(self) -> str:
        return self.aggregate_id
    
    @staticmethod
    def get_name() -> str:
        return 'homestock.catalogue.1.event.format.created'