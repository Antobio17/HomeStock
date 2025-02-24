
from dataclasses import dataclass
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.catalogue.product.domain.model.product_repository import ProductRepository
from src.catalogue.product.application.command.change_equivalence_units_command import ChangeEquivalenceUnitsCommand
from src.catalogue.product.domain.exception.change_equivalence_units_exception import ChangeEquivalenceUnitsException

@dataclass
class ChangeEquivalenceUnitsCommandHandler:
    __product_repository: ProductRepository
    __message_publisher: MessagePublisher

    def handle(self, command: ChangeEquivalenceUnitsCommand):
        product = self.__product_repository.find_by_id(command.id)
        if product is None:
            raise ChangeEquivalenceUnitsException(
                f'Product with ID {command.id} not found'
                f'productWithID{command.id}NotFound'
            )
            
        product.change_equivalence_units(
            command.recipe_unit,
            command.storage_unit,
            command.storage_unit_equivalence,
            command.purchase_unit,
            command.purchase_unit_equivalence
        )
        
        self.__product_repository.save(product)
        for event in product.pull_domain_events():
            self.__message_publisher.execute(event)