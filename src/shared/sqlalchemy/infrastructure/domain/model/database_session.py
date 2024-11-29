import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from src.catalogue.product.infrastructure.domain.model.sqlalchemy.persistence.model import ProductModel

class DatabaseSession:
    def __init__(self) -> None:            
        load_dotenv('/app/.env')
        load_dotenv('/app/.env.local')
        

    @property
    def writer_session(self) -> Session:
        engine = create_engine(os.getenv('DATABASE_WRITER_URL'), future=True, echo=True)
        session_factory = sessionmaker(bind=engine, future=True)
        return session_factory()
    
    @property
    def reader_session(self) -> Session:
        engine = create_engine(os.getenv('DATABASE_READER_URL'), future=True, echo=True)
        session_factory = sessionmaker(bind=engine, future=True)
        return session_factory()