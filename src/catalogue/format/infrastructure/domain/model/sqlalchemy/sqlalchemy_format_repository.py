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
    def __to_model(fmt: Format) -> FormatModel:
        return FormatModel(
            id = fmt.id,
            product_id = fmt.product_id,
            name = fmt.name,
            recipe_unit = fmt.recipe_unit,
            storage_unit = fmt.storage_unit,
            storage_unit_equivalence = fmt.storage_unit_equivalence,
            purchase_unit = fmt.purchase_unit,
            purchase_unit_equivalence = fmt.purchase_unit_equivalence,
            is_enabled = fmt.is_enabled,
            created_at = fmt.created_at,
            updated_at = fmt.updated_at,
            enabled_at = fmt.enabled_at,
            disabled_at = fmt.disabled_at
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

    def save(self, fmt: Format) -> None:
        self.__transaction_manager.session.merge(self.__to_model(fmt))