from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from src.shared.cqrs.domain.event.domain_event import DomainEvent
from src.catalogue.product.domain.event.product_created import ProductCreated
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
    
    def __init__(self):
        self.domain_events = []
        
    def record(self, domain_event: DomainEvent) -> None:
        self.domain_events.append(domain_event)
        
    def pull_domain_events(self) -> list[DomainEvent]:
        domain_events = self.domain_events
        self.domain_events = []
        return domain_events
    
    @staticmethod
    def create(
        id: str,
        name: str,
        price: float,
        calories: int,
        carbohydrates: int,
        proteins: int,
        fats: int,
        sugar: int,
        is_enabled: bool,
        created_at: datetime,
        enabled_at: datetime
    ) -> 'Product':
        if len(name) > 64:
            raise CreateProductException(
                'Name only accepts 64 characters', 
                'nameOnlyAccepts64Characters'
            )
   
        product = Product(
            id,
            name,
            price,
            calories,
            carbohydrates,
            proteins,
            fats,
            sugar,
            is_enabled,
            created_at,
            enabled_at,
            datetime.now(),
            datetime.now()
        )
        product.record(ProductCreated(
            id,
            name,
            price,
            calories,
            carbohydrates,
            proteins,
            fats,
            sugar,
            is_enabled,
            created_at,
            enabled_at                              
        ))
        
        return product
