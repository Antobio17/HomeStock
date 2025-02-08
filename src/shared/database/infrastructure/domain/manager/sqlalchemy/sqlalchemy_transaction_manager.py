import os
from src import thread_local
from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker # type: ignore
from src.shared.database.domain.manager.transaction_manager import TransactionManager

@dataclass
class SqlalchemyTransactionManager(TransactionManager):
    __database_writer_url: str = os.getenv('DATABASE_WRITER_URL')
    __session: Session = None
    __engine: Session = None
    
    @property
    def session(self) -> Session:
        schema = getattr(thread_local, 'schema_name', None)
        if self.__engine is None:
            self.__engine = create_engine(self.__database_writer_url + schema, future=True, echo=True)
        if self.__session is None:
            session_factory = sessionmaker(bind=self.__engine, future=True)
            self.__session = session_factory()
            
        return self.__session
    
    
    def begin(self):
        self.session.begin()
        
    def commit(self):
        self.session.commit()
        
    def close(self):
        self.__session.close()
        self.__session = None
        self.__engine.dispose()
        self.__engine = None
    