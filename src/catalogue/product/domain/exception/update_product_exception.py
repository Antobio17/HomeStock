from dataclasses import dataclass

@dataclass
class UpdateProductException(Exception):
    message: str
    keyTraslate: str