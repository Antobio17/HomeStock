from datetime import datetime
from dataclasses import dataclass
from src.shared.cqrs.domain.event.domain_event import DomainEvent

@dataclass
class NutritionFactsChanged(DomainEvent):
    aggregate_id: str
    calories: float
    carbohydrates: float
    proteins: float
    fats: float
    sugar: float
    updated_at: datetime
    
    def get_aggregate_id(self) -> str:
        return self.aggregate_id
    
    @staticmethod
    def get_name() -> str:
        return 'homestock.catalogue.1.event.product.nutrition_facts_changed'
