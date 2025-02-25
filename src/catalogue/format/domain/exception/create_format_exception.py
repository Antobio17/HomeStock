from dataclasses import dataclass

@dataclass
class CreateFormatException(Exception):
    message: str
    keyTraslate: str