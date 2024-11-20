
from src.shared.cqrs.application.command import Command


class CreateProductCommand(Command):
    def __init__(self, product_id: str, product_name: str):
        self.product_id = product_id
        self.product_name = product_name