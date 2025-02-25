from dataclasses import dataclass

@dataclass
class ChangeEquivalenceUnitsCommand:
    id: str
    recipe_unit: str
    storage_unit: str
    storage_unit_equivalence: float
    purchase_unit: str
    purchase_unit_equivalence: float
    purchase_price: float
