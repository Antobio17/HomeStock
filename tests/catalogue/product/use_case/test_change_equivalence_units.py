import uuid
import unittest
from datetime import datetime
from unittest.mock import Mock
from src.catalogue.product.domain.model.product import Product
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.catalogue.product.domain.event.equivalence_units_changed import EquivalenceUnitsChanged
from src.catalogue.product.application.command.change_equivalence_units_command import ChangeEquivalenceUnitsCommand
from src.catalogue.product.domain.exception.change_equivalence_units_exception import ChangeEquivalenceUnitsException
from src.catalogue.product.infrastructure.domain.model.in_memory.in_memory_product_repository import InMemoryProductRepository
from src.catalogue.product.application.command.change_equivalence_units_command_handler import ChangeEquivalenceUnitsCommandHandler

class TestEquivalenceUnits(unittest.TestCase):

    def setUp(self):
        self.__message_publisher = Mock(spec=MessagePublisher)

    def test_equivalence_units_success(self):
        id = str(uuid.uuid4())
        in_memory_repository = InMemoryProductRepository()
        in_memory_repository.will_return(
            Product(
                id = id,
                name = 'Test Product',
                recipe_unit = 'Test recipe unit',
                storage_unit = 'Test storage unit',
                storage_unit_equivalence = 1.0,
                purchase_unit = 'Test purchase unit',
                purchase_unit_equivalence = 1.0,
                is_enabled = True,
                created_at = datetime.now(),
                updated_at = None,
                enabled_at = datetime.now(),
                disabled_at = None
            )
        )
        
        command = ChangeEquivalenceUnitsCommand(
            id = id,
            recipe_unit = 'New recipe unit',
            storage_unit = 'New storage unit',
            storage_unit_equivalence = 10.0,
            purchase_unit = 'New purchase unit',
            purchase_unit_equivalence = 10.0
        )
        command_handler = ChangeEquivalenceUnitsCommandHandler(
            in_memory_repository,
            self.__message_publisher
        )
        command_handler.handle(command)
        
        product = in_memory_repository.spy()

        self.assertTrue(uuid.UUID(product.id))
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.price, 0)
        self.assertEqual(product.calories, 0)
        self.assertEqual(product.carbohydrates, 0)
        self.assertEqual(product.proteins, 0)
        self.assertEqual(product.fats, 0)
        self.assertEqual(product.sugar, 0)
        self.assertEqual(product.recipe_unit, command.recipe_unit)
        self.assertEqual(product.storage_unit, command.storage_unit)
        self.assertEqual(product.storage_unit_equivalence, command.storage_unit_equivalence)
        self.assertEqual(product.purchase_unit, command.purchase_unit)
        self.assertEqual(product.purchase_unit_equivalence, command.purchase_unit_equivalence)
        self.assertEqual(product.is_enabled, True)
        self.assertIsInstance(product.created_at, datetime)
        self.assertIsInstance(product.enabled_at, datetime)
        self.assertIsNotNone(product.updated_at)
        self.assertIsInstance(product.updated_at, datetime)
        self.assertIsNone(product.disabled_at)
        self.__message_publisher.execute.assert_called_once_with(
            EquivalenceUnitsChanged(
                product.id,
                product.recipe_unit,
                product.storage_unit,
                product.storage_unit_equivalence,
                product.purchase_unit,
                product.purchase_unit_equivalence,
                product.updated_at
            )
        )

    def test_update_product_negative_values(self):
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
        
        command = ChangeEquivalenceUnitsCommand(
            id = id,
            recipe_unit = 'New recipe unit',
            storage_unit = 'New storage unit',
            storage_unit_equivalence = 0.0,
            purchase_unit = 'New purchase unit',
            purchase_unit_equivalence = 0.0
        )
        command_handler = ChangeEquivalenceUnitsCommandHandler(
            in_memory_repository,
            self.__message_publisher
        )
        with self.assertRaises(ChangeEquivalenceUnitsException) as context:
            command_handler.handle(command)
        
        self.assertEqual(context.exception.message, 'Equivalence values must be greater than or equal to 1')
        self.assertEqual(context.exception.keyTraslate, 'equivalenceValuesMustBeGreaterThanOrEqualToOne')
        self.assertIsNone(in_memory_repository.spy())
        self.__message_publisher.execute.assert_not_called()


if __name__ == '__main__':
    unittest.main()