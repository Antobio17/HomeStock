from typing import Optional, Union
from dataclasses import dataclass
from src.shared.cqrs.application.query.query import Query

@dataclass
class GetProductsQuery(Query):
    name: Optional[Union[str, None]]
    price: Optional[Union[float, dict, None]]
    calories: Optional[Union[float, dict, None]]
    carbohydrates: Optional[Union[float, dict, None]]
    proteins: Optional[Union[float, dict, None]]
    fats: Optional[Union[float, dict, None]]
    sugar: Optional[Union[float, dict, None]]
    is_enabled: bool
    page: int
    page_size: int