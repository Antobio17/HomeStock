from src.catalogue.product.domain.repositories.product_repository import ProductRepository

class InMemoryProductRepository(ProductRepository):
    
    def __init__(self):
        self.products = {}

    def findById(self, id: str):
        return self.products.get(id)

    def findAll(self):
        return list(self.products.values())

    def save(self, product):
        self.products[product['id']] = product