from dataclasses import dataclass

@dataclass
class ChangeEquivalenceUnitsException(Exception):
    message: str
    key_translate: str