from datetime import datetime
from dataclasses import dataclass
from src.shared.cqrs.domain.service.dto.message import Message
from src.shared.cqrs.domain.event.domain_event import DomainEvent

@dataclass
class ProductUpdated(DomainEvent, Message):
    aggregate_id: str
    name: str
    price: float
    calories: int
    carbohydrates: int
    proteins: int
    fats: int
    sugar: int
    updated_at: datetime
    
    def get_aggregate_id(self) -> str:
        return self.aggregate_id
    
    @staticmethod
    def get_name() -> str:
        return 'homestock.catalogue.1.event.product.updated'
