import uuid
import unittest
from datetime import datetime
from unittest.mock import Mock
from src.catalogue.product.domain.model.product import Product
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.catalogue.product.domain.event.nutrition_facts_changed import NutritionFactsChanged
from src.catalogue.product.application.command.change_nutrition_facts_command import ChangeNutritionFactsCommand
from src.catalogue.product.domain.exception.change_nutrition_facts_exception import ChangeNutritionFactsException
from src.catalogue.product.application.command.change_nutrition_facts_command_handler import ChangeNutritionFactsCommandHandler
from src.catalogue.product.infrastructure.domain.model.in_memory.in_memory_product_repository import InMemoryProductRepository

class TestChangeNutritionFactsCommand(unittest.TestCase):

    def setUp(self):
        self.__message_publisher = Mock(spec=MessagePublisher)

    def test_change_nutrition_facts_success(self):
        id = str(uuid.uuid4())
        in_memory_repository = InMemoryProductRepository()
        in_memory_repository.will_return(
            Product(
                id = id,
                name = 'Test Product',
                calories = 0,
                carbohydrates = 0,
                proteins = 0,
                fats = 0,
                sugar = 0,
                is_enabled = True,
                created_at = datetime.now(),
                updated_at = None,
                enabled_at = datetime.now(),
                disabled_at = None
            )
        )
        
        command = ChangeNutritionFactsCommand(
            id = id,
            calories = 10,
            carbohydrates = 10,
            proteins = 10,
            fats = 10,
            sugar = 10
        )
        command_handler = ChangeNutritionFactsCommandHandler(
            in_memory_repository,
            self.__message_publisher
        )
        command_handler.handle(command)
        
        product = in_memory_repository.spy()

        self.assertTrue(uuid.UUID(product.id))
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.calories, command.calories)
        self.assertEqual(product.carbohydrates, command.carbohydrates)
        self.assertEqual(product.proteins, command.proteins)
        self.assertEqual(product.fats, command.fats)
        self.assertEqual(product.sugar, command.sugar)
        self.assertEqual(product.is_enabled, True)
        self.assertIsInstance(product.created_at, datetime)
        self.assertIsInstance(product.enabled_at, datetime)
        self.assertIsNotNone(product.updated_at)
        self.assertIsInstance(product.updated_at, datetime)
        self.assertIsNone(product.disabled_at)
        self.__message_publisher.execute.assert_called_once_with(
            NutritionFactsChanged(
                product.id,
                product.calories,
                product.carbohydrates,
                product.proteins,
                product.fats,
                product.sugar,
                product.updated_at
            )
        )
        
    def test_change_nutrition_facts_product_does_not_exist(self):
        id = str(uuid.uuid4())
        in_memory_repository = InMemoryProductRepository()
        
        command = ChangeNutritionFactsCommand(
            id = id,
            calories = 10,
            carbohydrates = 10,
            proteins = 10,
            fats = 10,
            sugar = -10
        )
        command_handler = ChangeNutritionFactsCommandHandler(
            in_memory_repository,
            self.__message_publisher
        )
        with self.assertRaises(ChangeNutritionFactsException) as context:
            command_handler.handle(command)
        
        self.assertEqual(context.exception.message, f'Product with ID {command.id} not found')
        self.assertEqual(context.exception.key_translate, f'productWithID{command.id}NotFound')
        self.assertIsNone(in_memory_repository.spy())
        self.__message_publisher.execute.assert_not_called()

    def test_change_nutrition_facts_negative_values(self):
        id = str(uuid.uuid4())
        in_memory_repository = InMemoryProductRepository()
        in_memory_repository.will_return(
            Product(
                id = id,
                name = 'Test Product',
                created_at = datetime.now(),
                enabled_at = datetime.now()
            )
        )
        
        command = ChangeNutritionFactsCommand(
            id = id,
            calories = 10,
            carbohydrates = 10,
            proteins = 10,
            fats = 10,
            sugar = -10
        )
        command_handler = ChangeNutritionFactsCommandHandler(
            in_memory_repository,
            self.__message_publisher
        )
        with self.assertRaises(ChangeNutritionFactsException) as context:
            command_handler.handle(command)
        
        self.assertEqual(context.exception.message, 'All numeric fields must be greater than or equal to 0')
        self.assertEqual(context.exception.key_translate, 'allNumericFieldsMustBeGreaterThanOrEqualToZero')
        self.assertIsNone(in_memory_repository.spy())
        self.__message_publisher.execute.assert_not_called()


if __name__ == '__main__':
    unittest.main()