from typing import Union
from dataclasses import dataclass, field
from src.catalogue.product.domain.model.product import Product
from src.catalogue.product.domain.model.product_repository import ProductRepository

@dataclass
class InMemoryProductRepository(ProductRepository):
    products: dict = field(default_factory=dict)

    def find_by_id(self, id: str) -> Union[Product, None]:
        return self.products.get(id)

    def save(self, product: Product) -> None:
        self.products[product['id']] = product
