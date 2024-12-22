from datetime import datetime
from dataclasses import dataclass
from src.shared.cqrs.domain.service.dto.message import Message
from src.shared.cqrs.domain.event.domain_event import DomainEvent
@dataclass
class ProductCreated(DomainEvent, Message):
    aggregate_id: str
    name: str
    price: float
    calories: int
    carbohydrates: int
    proteins: int
    fats: int
    sugar: int
    is_enabled: bool
    created_at: datetime
    enabled_at: datetime
    
    def get_aggregate_id(self) -> str:
        return self.aggregate_id
    
    @property
    def routing_key(self) -> str:
        return 'homestock.catalogue.1.event.product.created'