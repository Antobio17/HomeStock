from sqlalchemy import CHAR, Column, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ConnfigurationModel(Base):
    __tablename__ = 'configuration'
    
    id = Column(CHAR(36), primary_key = True)
    code = Column(CHAR(32), nullable = False)
    payload = Column(JSON, nullable = False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)