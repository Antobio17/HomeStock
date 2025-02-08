from abc import ABC, abstractmethod
from src.shared.cqrs.application.query.query import Query
from src.catalogue.product.domain.query_model.dto.get_product_result import GetProductResult

class GetProductsQueryModel(ABC):
    
    @abstractmethod
    def get(self, query: Query) -> list[GetProductResult]:
        pass
    
    @abstractmethod
    def count(self, query: Query) -> int:
        pass