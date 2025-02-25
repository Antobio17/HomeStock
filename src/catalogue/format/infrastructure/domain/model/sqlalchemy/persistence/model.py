from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy import CHAR, Column, DateTime, Boolean, Float

Base = declarative_base()

class FormatModel(Base):
    __tablename__ = 'format'
    
    id = Column(CHAR(36), primary_key = True)
    product_id = Column(CHAR(36), nullable = False)
    name = Column(CHAR(64),  nullable = False)
    recipe_unit = Column(CHAR(64),  nullable = False, default = '')
    storage_unit = Column(CHAR(64),  nullable = True, default = '')
    storage_unit_equivalence = Column(Float, nullable=False, default = 1.0)
    purchase_unit = Column(CHAR(64),  nullable = True, default = '')
    purchase_unit_equivalence = Column(Float, nullable=False, default = 1.0)
    purchase_price = Column(Float, nullable = False, default = 0.0)
    is_enabled = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    enabled_at = Column(DateTime, nullable=False)
    disabled_at = Column(DateTime, nullable=True)
    
    def __str__(self) -> str:
        return (
            f"""
            FormatModel(
                id = {self.id}, 
                product_id = {self.product_id},
                name = {self.name},
                recipe_unit = {self.recipe_unit},
                storage_unit = {self.storage_unit},
                storage_unit_equivalence = {self.storage_unit_equivalence},
                purchase_unit = {self.purchase_unit},
                purchase_unit_equivalence = {self.purchase_unit_equivalence},
                purchase_price = {self.purchase_price},
                is_enabled = {self.is_enabled},
                created_at = {self.created_at},	
                updated_at = {self.updated_at},
                enabled_at = {self.enabled_at},
                disabled_at = {self.disabled_at}
            )
            """
        )