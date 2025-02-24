from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy import CHAR, Column, DateTime, Boolean, Float, Integer

Base = declarative_base()

class ProductModel(Base):
    __tablename__ = 'product'
    
    id = Column(CHAR(36), primary_key = True)
    name = Column(CHAR(64),  nullable = False)
    price = Column(Float, nullable = False)
    calories = Column(Float, nullable = False, default = 0.0)
    carbohydrates = Column(Float, nullable = False, default = 0.0)
    proteins = Column(Float, nullable = False, default = 0.0)
    fats = Column(Float, nullable = False, default = 0.0)
    sugar = Column(Float, nullable = False, default = 0.0)
    recipe_unit = Column(CHAR(64),  nullable = False, default = '')
    storage_unit = Column(CHAR(64),  nullable = True, default = '')
    storage_unit_equivalence = Column(Float, nullable=False, default = 1.0)
    purchase_unit = Column(CHAR(64),  nullable = True, default = '')
    purchase_unit_equivalence = Column(Float, nullable=False, default = 1.0)
    is_enabled = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    enabled_at = Column(DateTime, nullable=False)
    disabled_at = Column(DateTime, nullable=True)
    
    def __str__(self) -> str:
        return (
            f"""
            ProductModel(
                id = {self.id}, 
                price = {self.price},
                calories = {self.calories},
                carbohydrates = {self.carbohydrates},
                proteins = {self.proteins},
                fats = {self.fats},
                sugar = {self.sugar}, 
                recipe_unit = {self.recipe_unit},
                storage_unit = {self.storage_unit},
                storage_unit_equivalence = {self.storage_unit_equivalence},
                purchase_unit = {self.purchase_unit},
                purchase_unit_equivalence = {self.purchase_unit_equivalence},
                is_enabled = {self.is_enabled},
                created_at = {self.created_at},	
                updated_at = {self.updated_at},
                enabled_at = {self.enabled_at},
                disabled_at = {self.disabled_at}
            )
            """
        )