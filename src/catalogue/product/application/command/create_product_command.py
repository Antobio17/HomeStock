from dataclasses import dataclass
from src.shared.cqrs.domain.service.dto.message import Message
from src.shared.cqrs.application.command.command import Command

@dataclass
class CreateProductCommand(Command, Message):
    name: str
    price: float
    calories: int
    carbohydrates: int
    proteins: int
    fats: int
    sugar: int
    
    @staticmethod
    def get_name() -> str:
        return 'homestock.catalogue.1.command.product.create'