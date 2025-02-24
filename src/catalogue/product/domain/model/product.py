import uuid
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
from src.shared.cqrs.domain.event.domain_event import DomainEvent
from src.catalogue.product.domain.event.product_created import ProductCreated
from src.catalogue.product.domain.event.nutrition_facts_changed import NutritionFactsChanged
from src.catalogue.product.domain.event.equivalence_units_changed import EquivalenceUnitsChanged
from src.catalogue.product.domain.exception.create_product_exception import CreateProductException
from src.catalogue.product.domain.exception.change_nutrition_facts_exception import ChangeNutritionFactsException
from src.catalogue.product.domain.exception.change_equivalence_units_exception import ChangeEquivalenceUnitsException

@dataclass
class Product:
    id: str
    name: str
    created_at: datetime
    enabled_at: datetime
    is_enabled: bool = True
    price: float = 0
    calories: float = 0
    carbohydrates: float = 0
    proteins: float = 0
    fats: float = 0
    sugar: float = 0
    recipe_unit: str = ''
    storage_unit: str = ''
    storage_unit_equivalence: float = 1.0
    purchase_unit: str = ''
    purchase_unit_equivalence: float = 1.0
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
    def create(name: str) -> 'Product':
        if len(name) > 64:
            raise CreateProductException(
                'Name only accepts 64 characters', 
                'nameOnlyAccepts64Characters'
            )
        
        id = str(uuid.uuid4())
        now = datetime.now()
        product = Product(
            id,
            name,
            created_at = now,
            enabled_at = now
        )

        product.record(
            ProductCreated(
                id,
                name,
                product.created_at,
                product.enabled_at                              
            )
        )

        return product

    def change_nutrition_facts(
        self,
        calories: float,
        carbohydrates: float,
        proteins: float,
        fats: float,
        sugar: float
    ) -> None:
        if any(value < 0 for value in [
            calories, carbohydrates, proteins, fats, sugar
        ]):
            raise ChangeNutritionFactsException(
                'All numeric fields must be greater than or equal to 0',
                'allNumericFieldsMustBeGreaterThanOrEqualToZero'
            )

        self.calories = calories
        self.carbohydrates = carbohydrates
        self.proteins = proteins
        self.fats = fats
        self.sugar = sugar
        self.updated_at = datetime.now()
        
        self.record(
            NutritionFactsChanged(
                self.id,
                calories,
                carbohydrates,
                proteins,
                fats,
                sugar,
                self.updated_at
            )
        )
        
    def change_equivalence_units(
        self,
        recipe_unit: str,
        storage_unit: str,
        storage_unit_equivalence: float,
        purchase_unit: str,
        purchase_unit_equivalence: float
    ) -> None:
        if any(value < 1 for value in [
            storage_unit_equivalence, purchase_unit_equivalence
        ]):
            raise ChangeEquivalenceUnitsException(
                'Equivalence values must be greater than or equal to 1',
                'equivalenceValuesMustBeGreaterThanOrEqualToOne'
            )

        self.recipe_unit = recipe_unit
        self.storage_unit = storage_unit
        self.storage_unit_equivalence = storage_unit_equivalence
        self.purchase_unit = purchase_unit
        self.purchase_unit_equivalence = purchase_unit_equivalence
        self.updated_at = datetime.now()
        
        self.record(
            EquivalenceUnitsChanged(
                self.id,
                recipe_unit,
                storage_unit,
                storage_unit_equivalence,
                purchase_unit,
                purchase_unit_equivalence,
                self.updated_at
            )
        )