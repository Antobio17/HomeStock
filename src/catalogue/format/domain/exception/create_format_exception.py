from dataclasses import dataclass

@dataclass
class CreateFormatException(Exception):
    message: str
    key_translate: str