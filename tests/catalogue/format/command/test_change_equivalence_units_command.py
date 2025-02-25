import uuid
import unittest
from datetime import datetime
from unittest.mock import Mock
from src.catalogue.format.domain.model.format import Format
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.catalogue.format.domain.event.equivalence_units_changed import EquivalenceUnitsChanged
from src.catalogue.format.application.command.change_equivalence_units_command import ChangeEquivalenceUnitsCommand
from src.catalogue.format.domain.exception.change_equivalence_units_exception import ChangeEquivalenceUnitsException
from src.catalogue.format.infrastructure.domain.model.in_memory.in_memory_format_repository import InMemoryFormatRepository
from src.catalogue.format.application.command.change_equivalence_units_command_handler import ChangeEquivalenceUnitsCommandHandler

class TestEquivalenceUnits(unittest.TestCase):

    def setUp(self):
        self.__message_publisher = Mock(spec=MessagePublisher)

    def test_equivalence_units_success(self):
        id = str(uuid.uuid4())
        in_memory_repository = InMemoryFormatRepository()
        in_memory_repository.will_return(
            Format(
                id = id,
                product_id = 'uuid',
                name = 'Test Format',
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
            purchase_unit_equivalence = 10.0,
            purchase_price = 10.0,
        )
        command_handler = ChangeEquivalenceUnitsCommandHandler(
            in_memory_repository,
            self.__message_publisher
        )
        command_handler.handle(command)
        
        format = in_memory_repository.spy()

        self.assertTrue(uuid.UUID(format.id))
        self.assertEqual(format.name, 'Test Format')
        self.assertEqual(format.product_id, 'uuid')
        self.assertEqual(format.recipe_unit, command.recipe_unit)
        self.assertEqual(format.storage_unit, command.storage_unit)
        self.assertEqual(format.storage_unit_equivalence, command.storage_unit_equivalence)
        self.assertEqual(format.purchase_unit, command.purchase_unit)
        self.assertEqual(format.purchase_unit_equivalence, command.purchase_unit_equivalence)
        self.assertEqual(format.purchase_price, command.purchase_price)
        self.assertEqual(format.is_enabled, True)
        self.assertIsInstance(format.created_at, datetime)
        self.assertIsInstance(format.enabled_at, datetime)
        self.assertIsNotNone(format.updated_at)
        self.assertIsInstance(format.updated_at, datetime)
        self.assertIsNone(format.disabled_at)
        self.__message_publisher.execute.assert_called_once_with(
            EquivalenceUnitsChanged(
                format.id,
                format.recipe_unit,
                format.storage_unit,
                format.storage_unit_equivalence,
                format.purchase_unit,
                format.purchase_unit_equivalence,
                format.purchase_price,
                format.updated_at
            )
        )

    def test_equivalence_units_values_less_than_one(self):
        id = str(uuid.uuid4())
        in_memory_repository = InMemoryFormatRepository()
        in_memory_repository.will_return(
            Format(
                id = id,
                product_id = 'uuid',
                name = 'Test Format',
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
            purchase_unit_equivalence = 0.0,
            purchase_price = 0.0
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