from dataclasses import dataclass
from src.shared.cqrs.application.command.command import Command

@dataclass
class CreateFormatCommand(Command):
    product_id: str
    name: str
    
    @staticmethod
    def get_name() -> str:
        return 'homestock.catalogue.1.command.format.create'