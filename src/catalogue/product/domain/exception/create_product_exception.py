from dataclasses import dataclass

@dataclass
class CreateProductException(Exception):
    message: str
    keyTraslate: str