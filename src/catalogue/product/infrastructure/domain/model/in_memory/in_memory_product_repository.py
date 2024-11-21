from dataclasses import dataclass, field
from src.catalogue.product.domain.repositories.product_repository import ProductRepository

@dataclass
class InMemoryProductRepository(ProductRepository):
    products: dict = field(default_factory=dict)

    def findById(self, id: str):
        return self.products.get(id)

    def findAll(self):
        return list(self.products.values())

    def save(self, product):
        self.products[product['id']] = product
