from dataclasses import dataclass
from src.shared.cqrs.application.command import Command

@dataclass
class CreateProductCommand(Command):
    product_id: str
    product_name: str