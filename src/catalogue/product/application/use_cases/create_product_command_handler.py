from typing import cast

from src.shared.cqrs.application.command_handler import CommandHandler
from src.catalogue.product.domain.repositories.product_repository import ProductRepository
from src.catalogue.product.infrastructure.domain.dependency_injector import ProductDependencyInjector
from src.catalogue.product.application.use_cases.create_product_command import CreateProductCommand


class CreateProductCommandHandler(CommandHandler):

    def __init__(self, dependency_injector: ProductDependencyInjector):
        self.product_repository = cast(ProductRepository, dependency_injector.getRepository(ProductRepository))


    def handle(self, command: CreateProductCommand) -> None:
        product = {
            'id': command.product_id,
            'name': command.product_name
        }
        self.product_repository.save(product)