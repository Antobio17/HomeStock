from typing import Union, Type
from dataclasses import dataclass
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import NoResultFound
from src.catalogue.product.domain.model.product import Product
from src.catalogue.product.domain.model.product_repository import ProductRepository
from src.catalogue.product.infrastructure.domain.model.sqlalchemy.persistence.model import ProductModel
from src.shared.database.infrastructure.domain.manager.sqlalchemy.sqlalchemy_transaction_manager import (
    SqlalchemyTransactionManager
)

@dataclass
class SqlalchemyProductRepository(ProductRepository):
    __transaction_manager: SqlalchemyTransactionManager

    @staticmethod
    def __to_model(product: Product) -> ProductModel:
        return ProductModel(
            id = product.id,
            name = product.name,
            calories = product.calories,
            carbohydrates = product.carbohydrates,
            proteins = product.proteins,
            fats = product.fats,
            sugar = product.sugar,
            is_enabled = product.is_enabled,
            created_at = product.created_at,
            updated_at = product.updated_at,
            enabled_at = product.enabled_at,
            disabled_at = product.disabled_at
        )

    def find_by_id(self, product_id: str) -> Union[Product, None]:
        try:
            result: Type[ProductModel] = (
                self.__transaction_manager.session.query(ProductModel)
                    .options(joinedload('*'))
                    .filter_by(id=str(product_id))
                    .one()
            )
        except NoResultFound:
            return None

        return Product(
            id = result.id,
            name = result.name,
            calories = result.calories,
            carbohydrates = result.carbohydrates,
            proteins = result.proteins,
            fats = result.fats,
            sugar = result.sugar,
            is_enabled = result.is_enabled,
            created_at = result.created_at,
            updated_at = result.updated_at,
            enabled_at = result.enabled_at,
            disabled_at = result.disabled_at
        )

    def save(self, product: Product) -> None:
        self.__transaction_manager.session.merge(self.__to_model(product))