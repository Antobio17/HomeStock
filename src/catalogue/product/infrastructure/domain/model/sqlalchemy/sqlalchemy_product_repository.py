from typing import Optional
from dataclasses import dataclass, field
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload
from catalogue.product.domain.model.product_repository import ProductRepository
from src.catalogue.product.infrastructure.domain.model.sqlalchemy.persistence.model import ProductModel
from src.catalogue.product.domain.model.product import Product

@dataclass
class SqlalchemyProductRepository(ProductRepository):
    session: Session

    def _to_model(self, product: Product) -> ProductModel:
        return ProductModel(
            id=product.id,
            price=product.price,
            calories=product.calories,
            carbohydrates=product.carbohydrates,
            proteins=product.proteins,
            fats=product.fats,
            sugar=product.sugar,
            is_enabled=product.is_enabled,
            created_at=product.created_at,
            updated_at=product.updated_at,
            enabled_at=product.enabled_at,
            disabled_at=product.disabled_at
        )

    def find_by_id(self, product_id: str) -> Optional[Product]:
        try:
            result: ProductModel = (
                self._session.query(ProductModel).options(joinedload("*")).filter_by(id=str(product_id)).one()
            )
        except NoResultFound:
            return None

        return Product(
            id=result.id,
            price=result.price,
            calories=result.calories,
            carbohydrates=result.carbohydrates,
            proteins=result.proteins,
            fats=result.fats,
            sugar=result.sugar,
            is_enabled=result.is_enabled,
            created_at=result.created_at,
            updated_at=result.updated_at,
            enabled_at=result.enabled_at,
            disabled_at=result.disabled_at
        )

    def save(self, product: {Product}) -> None:
        self._session.merge(self._to_model(product))