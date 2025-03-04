from typing import Union, Type
from dataclasses import dataclass
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import NoResultFound
from src.catalogue.format.domain.model.format import Format
from src.catalogue.format.domain.model.format_repository import FormatRepository
from src.catalogue.format.infrastructure.domain.model.sqlalchemy.persistence.model import FormatModel
from src.shared.database.infrastructure.domain.manager.sqlalchemy.sqlalchemy_transaction_manager import (
    SqlalchemyTransactionManager
)

@dataclass
class SqlalchemyFormatRepository(FormatRepository):
    __transaction_manager: SqlalchemyTransactionManager

    @staticmethod
    def __to_model(model: Format) -> FormatModel:
        return FormatModel(
            id = model.id,
            product_id = model.product_id,
            name = model.name,
            recipe_unit = model.recipe_unit,
            storage_unit = model.storage_unit,
            storage_unit_equivalence = model.storage_unit_equivalence,
            purchase_unit = model.purchase_unit,
            purchase_unit_equivalence = model.purchase_unit_equivalence,
            is_enabled = model.is_enabled,
            created_at = model.created_at,
            updated_at = model.updated_at,
            enabled_at = model.enabled_at,
            disabled_at = model.disabled_at
        )

    def find_by_id(self, format_id: str) -> Union[Format, None]:
        try:
            result: Type[FormatModel] = (
                self.__transaction_manager.session.query(FormatModel)
                    .options(joinedload('*'))
                    .filter_by(id=str(format_id)).one()
            )
        except NoResultFound:
            return None

        return Format(
            id = result.id,
            product_id = result.product_id,
            name = result.name,
            recipe_unit = result.recipe_unit,
            storage_unit = result.storage_unit,
            storage_unit_equivalence = result.storage_unit_equivalence,
            purchase_unit = result.purchase_unit,
            purchase_unit_equivalence = result.purchase_unit_equivalence,
            is_enabled = result.is_enabled,
            created_at = result.created_at,
            updated_at = result.updated_at,
            enabled_at = result.enabled_at,
            disabled_at = result.disabled_at
        )

    def save(self, model: Format) -> None:
        self.__transaction_manager.session.merge(self.__to_model(model))