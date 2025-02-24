from dataclasses import dataclass

@dataclass
class ChangeEquivalenceUnitsException(Exception):
    message: str
    keyTraslate: str