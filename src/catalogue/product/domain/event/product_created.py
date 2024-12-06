from datetime import datetime
from dataclasses import dataclass
from src.shared.cqrs.domain.event.domain_event import DomainEvent

@dataclass
class ProductCreated(DomainEvent):
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
    
    @staticmethod
    def event_name() -> str:
        return 'homestock.catalogue.1.event.product.created'