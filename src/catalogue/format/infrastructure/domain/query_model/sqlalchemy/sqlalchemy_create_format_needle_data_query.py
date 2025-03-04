from sqlalchemy.sql import text
from dataclasses import dataclass
from src.catalogue.format.domain.query_model.create_format_needle_data_query import CreateFormatNeedleDataQuery
from src.shared.database.infrastructure.domain.connection.sqlalchemy.sqlalchemy_reader_connection import (
    SqlalchemyReaderConnection
)

@dataclass
class SqlalchemyCreateFormatNeedleDataQuery(CreateFormatNeedleDataQuery):
    __connection: SqlalchemyReaderConnection
    
    def product_exists(self, product_id: str) -> bool:
        sql_query = f'SELECT id FROM product WHERE id = "{product_id}"'
        result = self.__connection.session.execute(text(sql_query)).fetchone()

        return result is not None