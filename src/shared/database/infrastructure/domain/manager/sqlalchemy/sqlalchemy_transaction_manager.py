import os
from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from src.shared.database.domain.manager.transaction_manager import TransactionManager

@dataclass
class SqlalchemyTransactionManager(TransactionManager):
    __session: Session = None
    
    @property
    def session(self) -> Session:
        if self.__session is None:
            engine = create_engine(os.getenv('DATABASE_WRITER_URL'), future=True, echo=True)
            session_factory = sessionmaker(bind=engine, future=True)
            self.__session = session_factory()
            
        return self.__session
    
    
    def begin(self):
        self.session.begin()
        
    def commit(self):
        self.session.commit()
    