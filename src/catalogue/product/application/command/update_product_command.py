from dataclasses import dataclass

@dataclass
class UpdateProductCommand:
    id: str
    name: str
    price: float
    calories: float
    carbohydrates: float
    proteins: float
    fats: float
    sugar: float
