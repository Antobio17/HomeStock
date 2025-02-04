from sqlalchemy import CHAR, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base # type: ignore

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'user'
    
    id = Column(CHAR(36), primary_key=True)
    email = Column(CHAR(255),  nullable=False)
    sub = Column(CHAR(255),  nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    def __str__(self) -> str:
        return (
            f"""
            ProductModel(
                id = {self.id}, 
                email = {self.email},
                sub = {self.sub},
                created_at = {self.created_at}
            )
            """
        )