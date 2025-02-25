from sqlalchemy.sql import text # type: ignore
from dataclasses import dataclass
from src.shared.database.domain.connection.connection import Connection
from src.catalogue.format.domain.query_model.create_format_needle_data_query import CreateFormatNeedleDataQuery


@dataclass
class SqlalchemyCreateFormatNeedleDataQuery(CreateFormatNeedleDataQuery):
    __connection: Connection
    
    def product_exists(self, product_id: str) -> bool:
        sql_query = f'SELECT id FROM product WHERE id = "{product_id}"'
        result = self.__connection.session.execute(text(sql_query)).fetchone()

        return result != None