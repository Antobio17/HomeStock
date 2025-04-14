from typing import Optional
from sqlalchemy.sql import text
from dataclasses import dataclass
from src.purchase.ticket.domain.query_model.validate_ticket_needle_data_query import ValidateTicketNeedleDataQuery
from src.shared.database.infrastructure.domain.connection.sqlalchemy.sqlalchemy_reader_connection import (
    SqlalchemyReaderConnection
)

@dataclass
class SqlalchemyValidateTicketNeedleDataQuery(ValidateTicketNeedleDataQuery):
    __connection: SqlalchemyReaderConnection
    
    def formats(self, format_names: list[str]) -> Optional[dict]:
        if len(format_names) == 0:
            return None
        
        sql_query = text(
            f"SELECT id, name FROM format WHERE name IN :format_names"
        ).params(format_names = format_names)
        result = self.__connection.session.execute(sql_query).fetchall()
        
        output = {}
        for format_id, name in result:
            output[name] = format_id
            
        return None if len(result) == 0 else output   
    
    def items(self, ticket_id: str) -> list[dict]:
        sql_query = text(
            f"SELECT id, description FROM ticket_item WHERE ticket_id = :ticket_id"
        ).params(ticket_id = ticket_id)
        result = self.__connection.session.execute(sql_query).fetchall()
        
        return [
            {
                'id': item_id,
                'description': description,
            } for item_id, description in result
        ] 
    

    
    