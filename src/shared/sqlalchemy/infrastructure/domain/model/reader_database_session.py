from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

@dataclass
class ReaderDatabaseSession:
    __url: str
    
    @property
    def session(self) -> Session:
        engine = create_engine(self.__url, future=True, echo=True)
        session_factory = sessionmaker(bind=engine, future=True)
        return session_factory()
    