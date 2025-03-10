from typing import Optional
from dataclasses import dataclass
from src.catalogue.product.domain.model.product import Product
from src.catalogue.product.domain.model.product_repository import ProductRepository

@dataclass
class InMemoryProductRepository(ProductRepository):
    __product: Product = None
    __saved: Product = None

    def find_by_id(self, product_id: str) -> Optional[Product]:
        if self.__product is None or self.__product.id != id:
            return None
        return self.__product

    def save(self, product: Product) -> None:
        self.__saved = product
        
    def spy(self) -> Product:
        return self.__saved
    
    def will_return(self, product: Product) -> None:
        self.__product = product
