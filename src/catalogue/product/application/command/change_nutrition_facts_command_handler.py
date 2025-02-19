
from dataclasses import dataclass
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.catalogue.product.domain.model.product_repository import ProductRepository
from src.catalogue.product.application.command.change_nutrition_facts_command import ChangeNutritionFactsCommand
from src.catalogue.product.domain.exception.change_nutrition_facts_exception import ChangeNutritionFactsException

@dataclass
class ChangeNutritionFactsCommandHandler:
    __product_repository: ProductRepository
    __message_publisher: MessagePublisher

    def handle(self, command: ChangeNutritionFactsCommand):
        product = self.__product_repository.find_by_id(command.id)
        if product is None:
            raise ChangeNutritionFactsException(
                f'Product with ID {command.id} not found'
                f'productWithID{command.id}NotFound'
            )
            
        product.change_nutrition_facts(
            command.calories,
            command.carbohydrates,
            command.proteins,
            command.fats,
            command.sugar
        )
        
        self.__product_repository.save(product)
        for event in product.pull_domain_events():
            self.__message_publisher.execute(event)