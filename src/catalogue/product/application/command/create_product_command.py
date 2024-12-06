from dataclasses import dataclass
from src.shared.cqrs.application.command.command import Command

@dataclass
class CreateProductCommand(Command):
    name: str
    price: float
    calories: int
    carbohydrates: int
    proteins: int
    fats: int
    sugar: int
    is_enabled: bool