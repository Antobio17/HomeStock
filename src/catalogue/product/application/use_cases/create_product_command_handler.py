from src.shared.cqrs.application.command_handler import CommandHandler
from src.catalogue.product.domain.repositories.product_repository import ProductRepository
from src.catalogue.product.application.use_cases.create_product_command import CreateProductCommand


class CreateProductCommandHandler(CommandHandler):

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository


    def handle(self, command: CreateProductCommand) -> None:
        product = {
            'id': command.product_id,
            'name': command.product_name
        }
        self.product_repository.save(product)