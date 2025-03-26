import uuid
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
from src.shared.cqrs.domain.event.domain_event import DomainEvent
from src.catalogue.format.domain.event.format_created import FormatCreated
from src.catalogue.format.domain.event.equivalence_units_changed import EquivalenceUnitsChanged
from src.catalogue.format.domain.exception.create_format_exception import CreateFormatException
from src.catalogue.format.domain.exception.change_equivalence_units_exception import ChangeEquivalenceUnitsException

@dataclass
class Format:
    id: str
    product_id: str
    name: str
    created_at: datetime
    enabled_at: datetime
    is_enabled: bool = True
    recipe_unit: str = ''
    storage_unit: str = ''
    storage_unit_equivalence: float = 1.0
    purchase_unit: str = ''
    purchase_unit_equivalence: float = 1.0
    purchase_price: float = 0.0
    updated_at: Optional[datetime] = None
    disabled_at: Optional[datetime] = None
    domain_events: list[DomainEvent] = field(default_factory = list)
    

    def record(self, domain_event: DomainEvent) -> None:
        self.domain_events.append(domain_event)
        
    def pull_domain_events(self) -> list[DomainEvent]:
        domain_events = self.domain_events
        self.domain_events = []
        return domain_events
    
    @staticmethod
    def create(product_id: str, name: str) -> 'Format':
        if len(name) > 64:
            raise CreateFormatException(
                'Name only accepts 64 characters', 
                'nameOnlyAccepts64Characters'
            )
        
        format_id = str(uuid.uuid4())
        now = datetime.now()
        fmt = Format(
            format_id,
            product_id,
            name,
            created_at = now,
            enabled_at = now
        )

        fmt.record(
            FormatCreated(
                format_id,
                product_id,
                name,
                fmt.created_at,
                fmt.enabled_at
            )
        )

        return fmt
    
    def change_equivalence_units(
        self,
        recipe_unit: str,
        storage_unit: str,
        storage_unit_equivalence: float,
        purchase_unit: str,
        purchase_unit_equivalence: float,
        purchase_price: float
    ) -> None:
        if any(value < 1 for value in [
            storage_unit_equivalence, purchase_unit_equivalence
        ]):
            raise ChangeEquivalenceUnitsException(
                'Equivalence values must be greater than or equal to 1',
                'equivalenceValuesMustBeGreaterThanOrEqualToOne'
            )
        if purchase_price < 0:
            raise ChangeEquivalenceUnitsException(
                'Purchase price must be greater than or equal to 0',
                'purchasePriceMustBeGreaterThanOrEqualToOne'
            )

        self.recipe_unit = recipe_unit
        self.storage_unit = storage_unit
        self.storage_unit_equivalence = storage_unit_equivalence
        self.purchase_unit = purchase_unit
        self.purchase_unit_equivalence = purchase_unit_equivalence
        self.purchase_price = purchase_price
        self.updated_at = datetime.now()
        
        self.record(
            EquivalenceUnitsChanged(
                self.id,
                recipe_unit,
                storage_unit,
                storage_unit_equivalence,
                purchase_unit,
                purchase_unit_equivalence,
                purchase_price,
                self.updated_at
            )
        )