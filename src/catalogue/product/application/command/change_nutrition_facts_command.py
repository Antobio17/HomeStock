from dataclasses import dataclass
from src.shared.cqrs.application.command.command import Command

@dataclass
class ChangeNutritionFactsCommand(Command):
    id: str
    calories: float
    carbohydrates: float
    proteins: float
    fats: float
    sugar: float
    
    @staticmethod
    def get_name() -> str:
        return 'homestock.catalogue.1.command.product.change_nutrition_facts'
