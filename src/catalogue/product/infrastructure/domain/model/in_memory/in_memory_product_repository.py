from typing import Union
from dataclasses import dataclass
from src.catalogue.product.domain.model.product import Product
from src.catalogue.product.domain.model.product_repository import ProductRepository

@dataclass
class InMemoryProductRepository(ProductRepository):
    product: Product = None

    def find_by_id(self, id: str) -> Union[Product, None]:
        if self.product == None or self.product.id != id:
            return None
        return self.product

    def save(self, product: Product) -> None:
        self.product = product
        
    def spy(self) -> Product:
        return self.product
    
    def will_return(self, product: Product) -> None:
        self.product = product
