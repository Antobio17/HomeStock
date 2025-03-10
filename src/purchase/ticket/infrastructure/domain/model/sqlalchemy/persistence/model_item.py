from sqlalchemy import CHAR, Column, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TicketItemModel(Base):
    __tablename__ = 'ticket_item'
    
    id = Column(CHAR(36), primary_key = True)
    ticket_id = Column(CHAR(36),  nullable = False)
    description = Column(CHAR(64),  nullable = False)
    quantity = Column(Float, nullable = False)
    unit_price = Column(Float, nullable = False)
    amount = Column(Float, nullable = False)
    format_id = Column(CHAR(36), nullable = True)
    product_id = Column(CHAR(36), nullable = True)