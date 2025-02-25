from datetime import datetime
from dataclasses import dataclass

@dataclass    
class GetProductResult:
    id: int
    name: str
    calories: float
    carbohydrates: float
    proteins: float
    fats: float
    sugar: float
    is_enabled: bool