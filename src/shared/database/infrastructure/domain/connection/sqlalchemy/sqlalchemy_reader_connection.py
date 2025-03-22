from typing import Optional
from src import thread_local
from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, sessionmaker
from src.shared.database.domain.connection.connection import Connection

@dataclass
class SqlalchemyReaderConnection(Connection):
    __database_reader_url: str
    __session: Optional[Session] = None
    __engine: Optional[Engine] = None
    
    @property
    def session(self) -> Session:
        schema = getattr(thread_local, 'schema_name', None)
        if self.__engine is None:
            self.__engine = create_engine(self.__database_reader_url + schema, future=True, echo=True)
        if self.__session is None:
            session_factory = sessionmaker(bind=self.__engine, future=True)
            self.__session = session_factory()
            
        return self.__session
    
    def close(self) -> None:
        if self.__session is not None:
            self.__session.close()
            self.__session = None
        if self.__engine is not None:
            self.__engine.dispose()
            self.__engine = None