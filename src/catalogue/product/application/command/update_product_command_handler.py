
from dataclasses import dataclass
from src.catalogue.product.domain.model.product import Product
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.catalogue.product.domain.model.product_repository import ProductRepository
from src.catalogue.product.application.command.update_product_command import UpdateProductCommand

@dataclass
class UpdateProductCommandHandler:
    __product_repository: ProductRepository
    __message_publisher: MessagePublisher

    def handle(self, command: UpdateProductCommand):
        product = Product.update(
            command = command,
            repository = self.__product_repository
        )
        
        for event in product.pull_domain_events():
            self.__message_publisher.execute(event)