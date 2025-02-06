import os
from src import thread_local
from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker # type: ignore
from src.shared.database.domain.manager.transaction_manager import TransactionManager

@dataclass
class SqlalchemyTransactionManager(TransactionManager):
    __session: Session = None
    __database_writer_url: str = os.getenv('DATABASE_WRITER_URL')
    
    @property
    def session(self) -> Session:
        schema = getattr(thread_local, 'schema_name', None)
        if self.__session is None:
            engine = create_engine(self.__database_writer_url + schema, future=True, echo=True)
            session_factory = sessionmaker(bind=engine, future=True)
            self.__session = session_factory()
            
        return self.__session
    
    
    def begin(self):
        self.session.begin()
        
    def commit(self):
        self.session.commit()
    