from sqlalchemy.sql import text # type: ignore
from dataclasses import dataclass
from src.shared.database.domain.connection.connection import Connection
from src.catalogue.product.application.query.get_products_query import GetProductsQuery
from src.catalogue.product.domain.query_model.dto.get_product_result import GetProductResult
from src.catalogue.product.domain.query_model.get_products_query_model import GetProductsQueryModel
from src.shared.utils.infrastructure.domain.service.utils import Utils

@dataclass
class SqlalchemyGetProductsQueryModel(GetProductsQueryModel):
    __connection: Connection
    
    def get(self, query: GetProductsQuery) -> list[GetProductResult]:
        sql_query = self.__build_sql(query)
        if query.page and query.page_size:
            sql_query += f' LIMIT {query.page_size} OFFSET {query.page_size * (query.page - 1)}'
        
        results = self.__connection.session.execute(text(sql_query)).fetchall()
        
        return [GetProductResult(*result) for result in results]

    def count(self, query: GetProductsQuery) -> int:
        sql_query = self.__build_sql(query, count = True)
        
        results = self.__connection.session.execute(text(sql_query)).fetchone()
        return results[0]
        
    
    def __build_sql(self, query: GetProductsQuery, count: bool = False) -> str:
        sql_query = """
        SELECT 
        id, name, price, calories, carbohydrates, 
        proteins, fats, sugar, is_enabled
        FROM product
        """
        if count:
            sql_query = 'SELECT COUNT(*) FROM product'
        
        where_clause = ' WHERE'
        if query.name is not None:
            where_clause += f' name = "{query.name}" AND'
        if query.price is not None:
            where_clause = Utils.add_condition_query(where_clause, 'price', query.price)
        if query.calories is not None:
            where_clause = Utils.add_condition_query(where_clause, 'calories', query.calories)
        if query.carbohydrates is not None:
            where_clause = Utils.add_condition_query(where_clause, 'carbohydrates', query.carbohydrates)
        if query.proteins is not None:
            where_clause = Utils.add_condition_query(where_clause, 'proteins', query.proteins)
        if query.fats is not None:
            where_clause = Utils.add_condition_query(where_clause, 'fats', query.fats)
        if query.sugar is not None:
            where_clause = Utils.add_condition_query(where_clause, 'sugar', query.sugar)
        where_clause += f' is_enabled = {1 if query.is_enabled else 0}'
        
        sql_query += where_clause
        return sql_query