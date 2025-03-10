from sqlalchemy.sql import text
from dataclasses import dataclass
from src.purchase.ticket.domain.query_model.submit_ticket_needle_data_query import SubmitTicketNeedleDataQuery
from src.shared.database.infrastructure.domain.connection.sqlalchemy.sqlalchemy_reader_connection import (
    SqlalchemyReaderConnection
)

@dataclass
class SqlalchemySubmitTicketNeedleDataQuery(SubmitTicketNeedleDataQuery):
    __connection: SqlalchemyReaderConnection
    
    def ticket_exists(self, reference: str) -> bool:
        sql_query = f'SELECT id FROM ticket WHERE reference = "{reference}"'
        result = self.__connection.session.execute(text(sql_query)).fetchone()

        return result is not None
    
    