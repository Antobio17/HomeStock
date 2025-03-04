from dataclasses import dataclass

@dataclass
class CreateProductException(Exception):
    message: str
    key_translate: str