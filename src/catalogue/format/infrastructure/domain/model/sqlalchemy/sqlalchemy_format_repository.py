from typing import Union
from dataclasses import dataclass
from sqlalchemy.orm import joinedload # type: ignore
from sqlalchemy.exc import NoResultFound # type: ignore
from src.catalogue.format.domain.model.format import Format
from src.catalogue.format.domain.model.format_repository import FormatRepository
from src.shared.database.domain.manager.transaction_manager import TransactionManager
from src.catalogue.format.infrastructure.domain.model.sqlalchemy.persistence.model import FormatModel

@dataclass
class SqlalchemyFormatRepository(FormatRepository):
    __transaction_manager: TransactionManager

    def __to_model(self, format: Format) -> FormatModel:
        return FormatModel(
            id = format.id,
            product_id = format.product_id,
            name = format.name,
            recipe_unit = format.recipe_unit,
            storage_unit = format.storage_unit,
            storage_unit_equivalence = format.storage_unit_equivalence,
            purchase_unit = format.purchase_unit,
            purchase_unit_equivalence = format.purchase_unit_equivalence,
            is_enabled = format.is_enabled,
            created_at = format.created_at,
            updated_at = format.updated_at,
            enabled_at = format.enabled_at,
            disabled_at = format.disabled_at
        )

    def find_by_id(self, format_id: str) -> Union[Format, None]:
        try:
            result: FormatModel = (
                self.__transaction_manager.session.query(FormatModel)\
                    .options(joinedload('*'))\
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

    def save(self, format: Format) -> None:
        self.__transaction_manager.session.merge(self.__to_model(format))