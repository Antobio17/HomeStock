import uuid
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
from src.shared.cqrs.domain.event.domain_event import DomainEvent
from src.catalogue.product.domain.event.product_created import ProductCreated
from src.catalogue.product.domain.event.product_updated import ProductUpdated
from src.catalogue.product.domain.model.product_repository import ProductRepository
from src.catalogue.product.application.command.create_product_command import CreateProductCommand
from src.catalogue.product.application.command.update_product_command import UpdateProductCommand
from src.catalogue.product.domain.exception.create_product_exception import CreateProductException
from src.catalogue.product.domain.exception.update_product_exception import UpdateProductException

@dataclass
class Product:
    id: str
    name: str
    price: float
    calories: float
    carbohydrates: float
    proteins: float
    fats: float
    sugar: float
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
    def create(
        command: CreateProductCommand,
        repository: ProductRepository
    ) -> 'Product':
        if len(command.name) > 64:
            raise CreateProductException(
                'Name only accepts 64 characters', 
                'nameOnlyAccepts64Characters'
            )
        if any(value < 0 for value in [
            command.price, command.calories, command.carbohydrates, 
            command.proteins, command.fats, command.sugar
        ]):
            raise CreateProductException(
                'All numeric fields must be greater than or equal to 0',
                'allNumericFieldsMustBeGreaterThanOrEqualToZero'
            )
   
        id = str(uuid.uuid4())
        now = datetime.now()
        product = Product(
            id = id,
            name = command.name,
            price = command.price,
            calories = command.calories,
            carbohydrates = command.carbohydrates,
            proteins = command.proteins,
            fats = command.fats,
            sugar = command.sugar,
            is_enabled = True,
            created_at = now,
            enabled_at = now
        )
        
        repository.save(product)
        product.record(
            ProductCreated(
                id = id,
                name = command.name,
                price = command.price,
                calories = command.calories,
                carbohydrates = command.carbohydrates,
                proteins = command.proteins,
                fats = command.fats,
                sugar = command.sugar,
                is_enabled = True,
                created_at = now,
                enabled_at = now                              
            )
        )

        return product

    @staticmethod
    def update(
        command: UpdateProductCommand, 
        repository: ProductRepository
    ) -> 'Product':
        product = repository.find_by_id(command.id)
        if product is None:
            raise UpdateProductException(
                f'Product with ID {command.id} not found'
                f'productWithID{command.id}NotFound'
            )
        if len(command.name) > 64:
            raise UpdateProductException(
                'Name only accepts 64 characters', 
                'nameOnlyAccepts64Characters'
            )
        if any(value < 0 for value in [
            command.price, command.calories, command.carbohydrates, 
            command.proteins, command.fats, command.sugar
        ]):
            raise UpdateProductException(
                'All numeric fields must be greater than or equal to 0',
                'allNumericFieldsMustBeGreaterThanOrEqualToZero'
            )

        product.name = command.name
        product.price = command.price
        product.calories = command.calories
        product.carbohydrates = command.carbohydrates
        product.proteins = command.proteins
        product.fats = command.fats
        product.sugar = command.sugar
        product.updated_at = datetime.now()
        
        repository.save(product)
        product.record(
            ProductUpdated(
                id = id,
                name = command.name,
                price = command.price,
                calories = command.calories,
                carbohydrates = command.carbohydrates,
                proteins = command.proteins,
                fats = command.fats,
                sugar = command.sugar,
                updated_at = product.updated_at
            )
        )
        
        return product
