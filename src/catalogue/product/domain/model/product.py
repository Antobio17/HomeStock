from typing import Optional
from datetime import datetime
from dataclasses import dataclass

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