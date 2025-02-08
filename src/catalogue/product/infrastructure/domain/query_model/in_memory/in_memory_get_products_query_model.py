from dataclasses import dataclass
from src.catalogue.product.application.query.get_products_query import GetProductsQuery
from src.catalogue.product.domain.query_model.dto.get_product_result import GetProductResult
from src.catalogue.product.domain.query_model.get_products_query_model import GetProductsQueryModel

@dataclass
class InMemoryGetProductsQueryModel(GetProductsQueryModel):
    
    def get(self, query: GetProductsQuery) -> list[GetProductResult]:
        return []
    
    def count(self, query: GetProductsQuery) -> int:
        return 0