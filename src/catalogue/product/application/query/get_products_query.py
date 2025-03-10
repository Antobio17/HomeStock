from typing import Optional, Union
from dataclasses import dataclass
from src.shared.cqrs.application.query.query import Query

@dataclass
class GetProductsQuery(Query):
    name: Optional[str]
    calories: Optional[Union[float, dict]]
    carbohydrates: Optional[Union[float, dict]]
    proteins: Optional[Union[float, dict]]
    fats: Optional[Union[float, dict]]
    sugar: Optional[Union[float, dict]]
    is_enabled: bool
    page: int
    page_size: int