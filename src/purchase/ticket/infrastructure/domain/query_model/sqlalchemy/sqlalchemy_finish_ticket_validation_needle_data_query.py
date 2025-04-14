from sqlalchemy.sql import text
from dataclasses import dataclass
from src.purchase.ticket.domain.query_model.finish_ticket_validation_needle_data_query import FinishTicketValidationNeedleDataQuery
from src.shared.database.infrastructure.domain.connection.sqlalchemy.sqlalchemy_reader_connection import (
    SqlalchemyReaderConnection
)

@dataclass
class SqlalchemyFinishTicketValidationNeedleDataQuery(FinishTicketValidationNeedleDataQuery):
    __connection: SqlalchemyReaderConnection
    
    def all_formats_exist(self, format_ids: list) -> bool:
        if len(format_ids) == 0:
            return True
        
        sql_query = text(
            f"SELECT COUNT(id) FROM format WHERE id IN :format_ids"
        ).params(format_ids = format_ids)
        result = self.__connection.session.execute(sql_query).scalar()

        return result == len(format_ids)
    

    
    