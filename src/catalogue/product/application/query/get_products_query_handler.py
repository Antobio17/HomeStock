from dataclasses import dataclass
from src.shared.cqrs.application.query.query_handler import QueryHandler
from src.shared.cqrs.application.query.dto.query_result import QueryResult
from src.catalogue.product.application.query.get_products_query import GetProductsQuery
from src.catalogue.product.domain.query_model.get_products_query_model import GetProductsQueryModel


@dataclass
class GetProductsQueryHandler(QueryHandler):
    __get_products_query: GetProductsQueryModel
    
    def handle(self, query: GetProductsQuery) -> QueryResult:
        result = self.__get_products_query.get(query)
        total = self.__get_products_query.count(query)
        
        return QueryResult(
            result = result,
            page = query.page,
            page_size = query.page_size,
            total = total
        )