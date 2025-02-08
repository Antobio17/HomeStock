from datetime import datetime, timezone
from dataclasses import dataclass
from src.catalogue.product.domain.model.product import Product
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.shared.cqrs.application.command.command_handler import CommandHandler
from src.catalogue.product.domain.model.product_repository import ProductRepository
from src.catalogue.product.application.command.create_product_command import CreateProductCommand

@dataclass
class CreateProductCommandHandler(CommandHandler):
    __product_repository: ProductRepository
    __message_publisher: MessagePublisher

    def handle(self, command: CreateProductCommand) -> None:
        product = Product.create(
            command,
            self.__product_repository
        )
        
        for event in product.pull_domain_events():
            self.__message_publisher.execute(event)