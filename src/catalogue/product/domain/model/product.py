from typing import Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Product:
    id: str
    price: float
    calories: int
    carbohydrates: int
    proteins: int
    fats: int
    sugar: int
    is_enabled: bool
    created_at: datetime
    updated_at: Optional[datetime]
    enabled_at: datetime
    disabled_at: Optional[datetime]  
    
    @property
    def id(self) -> str:
        return self.id
    
    @property
    def created_at(self) -> float:
        return self.created_at