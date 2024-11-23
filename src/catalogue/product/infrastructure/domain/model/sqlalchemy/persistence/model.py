from src.shared.sqlalchemy.infrastructure.domain.model.db import Base
from sqlalchemy import CHAR, Column, DateTime, Boolean, Float, Integer


class ProductModel(Base):
    __tablename__ = 'product'
    
    id = Column(CHAR(32), primary_key=True)
    price = Column(Float, nullable=False)
    calories = Column(Integer, nullable=False)
    carbohydrates = Column(Integer, nullable=False)
    proteins = Column(Integer, nullable=False)
    fats = Column(Integer, nullable=False)
    sugar = Column(Integer, nullable=False)
    is_enabled = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    enabled_at = Column(DateTime, nullable=False)
    disabled_at = Column(DateTime, nullable=True)
    
    def __str__(self) -> str:
        return (
            f"""
            ProductModel(
                id={self.id}, 
                price={self.price},
                calories={self.calories},
                carbohydrates={self.carbohydrates},
                proteins={self.proteins},
                fats={self.fats},
                sugar={self.sugar}, 
                is_enabled={self.is_enabled},
                created_at={self.created_at},	
                updated_at={self.updated_at},
                enabled_at={self.enabled_at},
                disabled_at={self.disabled_at}
            )
            """
        )