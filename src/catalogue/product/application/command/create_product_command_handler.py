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
        product = Product (
            command.id,
            command.name,
            command.price,
            command.calories,
            command.carbohydrates,
            command.proteins,
            command.fats,
            command.sugar,
            command.is_enabled,
            datetime.now(timezone.utc),
            datetime.now(timezone.utc),
        )
        self.product_repository.save(product)