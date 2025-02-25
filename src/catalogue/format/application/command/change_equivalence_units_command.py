from dataclasses import dataclass
from src.shared.cqrs.domain.service.dto.message import Message
from src.shared.cqrs.application.command.command import Command

@dataclass
class ChangeEquivalenceUnitsCommand(Command, Message):
    id: str
    recipe_unit: str
    storage_unit: str
    storage_unit_equivalence: float
    purchase_unit: str
    purchase_unit_equivalence: float
    purchase_price: float
    
    @staticmethod
    def get_name() -> str:
        return 'homestock.catalogue.1.command.format.change_equivalence_units'
