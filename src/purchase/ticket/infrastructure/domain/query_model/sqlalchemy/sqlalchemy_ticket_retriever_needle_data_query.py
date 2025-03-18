import json
from typing import Optional
from sqlalchemy.sql import text
from dataclasses import dataclass
from src.system.configuration.domain.model.configuration import TICKET_POOL
from src.purchase.ticket.domain.query_model.ticket_retriever_needle_data_query import TicketRetrieverNeedleDataQuery
from src.shared.database.infrastructure.domain.connection.sqlalchemy.sqlalchemy_reader_connection import (
    SqlalchemyReaderConnection
)

@dataclass
class SqlalchemyTicketRetrieverNeedleDataQuery(TicketRetrieverNeedleDataQuery):
    __connection: SqlalchemyReaderConnection
    
    def get_ticket_pool(self, supermarket: str) -> Optional[str]:
        sql_query = f'SELECT payload FROM configuration WHERE code = "{TICKET_POOL}"'
        result = self.__connection.session.execute(text(sql_query)).fetchone()

        if result is None:
            return
        
        payload = json.loads(result[0])
        return payload.get(supermarket, None)
    
    