from sqlalchemy.sql import text
from dataclasses import dataclass
from src.purchase.ticket.domain.query_model.validate_ticket_needle_data_query import ValidateTicketNeedleDataQuery
from src.shared.database.infrastructure.domain.connection.sqlalchemy.sqlalchemy_reader_connection import (
    SqlalchemyReaderConnection
)

@dataclass
class SqlalchemyValidateTicketNeedleDataQuery(ValidateTicketNeedleDataQuery):
    __connection: SqlalchemyReaderConnection
    
    def all_products_exist(self, product_ids: list) -> bool:
        if (len(product_ids) == 0):
            return True
        
        sql_query = text(
            f"SELECT COUNT(id) FROM product WHERE id IN :product_ids"
        ).params(product_ids = product_ids)
        result = self.__connection.session.execute(sql_query).scalar()

        return result == len(product_ids)
    
    def all_formats_exist(self, format_ids: list) -> bool:
        if (len(format_ids) == 0):
            return True
        
        sql_query = text(
            f"SELECT COUNT(id) FROM format WHERE id IN :format_ids"
        ).params(format_ids = format_ids)
        result = self.__connection.session.execute(sql_query).scalar()

        return result == len(format_ids)
    

    
    