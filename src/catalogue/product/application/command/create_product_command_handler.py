from datetime import datetime, timezone
from dataclasses import dataclass
from src.catalogue.product.domain.model.product import Product
from src.shared.cqrs.application.command.command_handler import CommandHandler
from src.catalogue.product.domain.model.product_repository import ProductRepository
from src.catalogue.product.application.command.create_product_command import CreateProductCommand

@dataclass
class CreateProductCommandHandler(CommandHandler):
    product_repository: ProductRepository

    def handle(self, command: CreateProductCommand) -> None:
        product = Product.create(command)
        self.product_repository.save(product)