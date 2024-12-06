import uuid
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
from src.shared.cqrs.domain.event.domain_event import DomainEvent
from src.catalogue.product.domain.event.product_created import ProductCreated
from src.catalogue.product.application.command.create_product_command import CreateProductCommand
from src.catalogue.product.domain.exception.create_product_exception import CreateProductException

@dataclass
class Product:
    id: str
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
    updated_at: Optional[datetime] = None
    disabled_at: Optional[datetime] = None
    domain_events: list[DomainEvent] = field(default_factory=list)
    

    def record(self, domain_event: DomainEvent) -> None:
        self.domain_events.append(domain_event)
        
    def pull_domain_events(self) -> list[DomainEvent]:
        domain_events = self.domain_events
        self.domain_events = []
        return domain_events
    
    @staticmethod
    def create(command: CreateProductCommand) -> 'Product':
        if len(command.name) > 64:
            raise CreateProductException(
                'Name only accepts 64 characters', 
                'nameOnlyAccepts64Characters'
            )
        if any(value < 0 for value in [
            command.calories, command.carbohydrates, command.proteins, command.fats, command.sugar
        ]):
            raise CreateProductException(
                'All numeric fields must be greater than or equal to 0',
                'allNumericFieldsMustBeGreaterThanOrEqualToZero'
            )
   
        id = str(uuid.uuid4())
        now = datetime.now()
        product = Product(
            id,
            command.name,
            command.price,
            command.calories,
            command.carbohydrates,
            command.proteins,
            command.fats,
            command.sugar,
            command.is_enabled,
            now,
            now
        )
        product.record(
            ProductCreated(
                id,
                command.name,
                command.price,
                command.calories,
                command.carbohydrates,
                command.proteins,
                command.fats,
                command.sugar,
                command.is_enabled,
                now,
                now                              
            )
        )

        return product
