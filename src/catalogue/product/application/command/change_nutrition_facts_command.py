from dataclasses import dataclass

@dataclass
class ChangeNutritionFactsCommand:
    id: str
    calories: float
    carbohydrates: float
    proteins: float
    fats: float
    sugar: float
