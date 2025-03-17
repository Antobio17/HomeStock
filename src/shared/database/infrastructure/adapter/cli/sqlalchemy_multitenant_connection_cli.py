import os
from src import thread_local
from dataclasses import dataclass
from abc import ABC, abstractmethod
from sqlalchemy import create_engine, text

@dataclass
class SqlalchemyMultitenantConnectionCli(ABC):
    __database_reader_url: str = os.getenv('DATABASE_READER_URL')
        
    @abstractmethod
    def execute(self) -> None:
        pass
    
    @property
    def __schemas(self) -> list[str]:
        engine = create_engine(self.__database_reader_url)
        sql = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA"
        
        with engine.connect() as connection:
            result = connection.execute(text(sql))
            schemas = result.fetchall() 
            
            tenants = [schema[0] for schema in schemas if schema[0].isdigit()]
            
            connection.close()
        engine.dispose()
        
        return tenants
        
    def execute_multitenant(self) -> None:
        for schema in self.__schemas:
            thread_local.schema_name = schema
            self.execute()