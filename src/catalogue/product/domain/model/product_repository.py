from typing import Optional
from abc import ABC, abstractmethod
from src.catalogue.product.domain.model.product import Product

class ProductRepository(ABC):

    @abstractmethod
    def find_by_id(self, product_id: str) -> Optional[Product]:
        pass

    @abstractmethod
    def save(self, product: Product)  -> None:
        pass