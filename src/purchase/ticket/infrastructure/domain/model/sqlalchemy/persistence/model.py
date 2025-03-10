from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import CHAR, Column, DateTime, JSON, Float

Base = declarative_base()

class TicketModel(Base):
    __tablename__ = 'ticket'
    
    id = Column(CHAR(36), primary_key = True)
    supermarket = Column(CHAR(64),  nullable = False)
    reference = Column(CHAR(64),  nullable = False)
    status = Column(CHAR(32),  nullable = False)
    subtotal = Column(Float, nullable = False)
    discount_amount = Column(Float, nullable = False)
    taxes = Column(JSON, nullable = False)
    tax_amount = Column(Float, nullable = False)
    total = Column(Float, nullable = False)
    purchased_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)