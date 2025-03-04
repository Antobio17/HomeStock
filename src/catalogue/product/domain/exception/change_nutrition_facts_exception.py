from dataclasses import dataclass

@dataclass
class ChangeNutritionFactsException(Exception):
    message: str
    key_translate: str