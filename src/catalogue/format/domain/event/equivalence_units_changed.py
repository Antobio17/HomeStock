from datetime import datetime
from dataclasses import dataclass
from src.shared.cqrs.domain.service.dto.message import Message
from src.shared.cqrs.domain.event.domain_event import DomainEvent

@dataclass
class EquivalenceUnitsChanged(DomainEvent, Message):
    aggregate_id: str
    recipe_unit: str
    storage_unit: str
    storage_unit_equivalence: float
    purchase_unit: str
    purchase_unit_equivalence: float
    purchase_price: float
    updated_at: datetime
    
    def get_aggregate_id(self) -> str:
        return self.aggregate_id
    
    @staticmethod
    def get_name() -> str:
        return 'homestock.catalogue.1.event.product.equivalence_units_changed'
