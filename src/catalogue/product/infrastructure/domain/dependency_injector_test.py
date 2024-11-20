from src.shared.dependency_injector.domain.dependendy_injector import (DependencyInjector, R,  S,  Q)
from src.catalogue.product.domain.repositories.product_repository import ProductRepository
from src.catalogue.product.infrastructure.domain.repositories.in_memory.in_memory_product_repository import InMemoryProductRepository

class TestProductDependencyInjector(DependencyInjector[R, S, Q]):

    def getRepository(self, repository: type[R]) -> R:
        if repository == ProductRepository:
            return InMemoryProductRepository()
    
    def getService(self, key: type[S]) -> S:
        pass
    
    def getQueryModel(self, key: type[Q]) -> Q:
        pass