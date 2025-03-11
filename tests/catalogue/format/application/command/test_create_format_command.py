import uuid
import unittest
from datetime import datetime
from unittest.mock import Mock
from src.catalogue.format.domain.model.format import Format
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.catalogue.format.domain.event.format_created import FormatCreated
from src.catalogue.format.application.command.create_format_command import CreateFormatCommand
from src.catalogue.format.domain.exception.create_format_exception import CreateFormatException
from src.catalogue.format.application.command.create_format_command_handler import CreateFormatCommandHandler
from src.catalogue.format.infrastructure.domain.model.in_memory.in_memory_format_repository import InMemoryFormatRepository
from src.catalogue.format.infrastructure.domain.query_model.in_memory.in_memory_create_format_needle_data_query import InMemoryCreateFormatNeedleDataQuery

class TestCreateFormatCommand(unittest.TestCase):

    def setUp(self):
        self.__message_publisher = Mock(spec=MessagePublisher)

    def test_create_format_when_no_errors_then_success(self):
        in_memory_repository = InMemoryFormatRepository()
        needle_data_query = InMemoryCreateFormatNeedleDataQuery()
        needle_data_query.will_return(True)
        
        command = CreateFormatCommand('uuid', 'Test Format')
        command_handler = CreateFormatCommandHandler(
            needle_data_query,
            in_memory_repository,
            self.__message_publisher
        )
        command_handler.handle(command)
        
        format = in_memory_repository.spy()

        self.assertIsInstance(format, Format)
        self.assertTrue(uuid.UUID(format.id))
        self.assertEqual(format.product_id, command.product_id)
        self.assertEqual(format.name, command.name)
        self.assertTrue(not format.recipe_unit)
        self.assertTrue(not format.storage_unit)
        self.assertEqual(format.storage_unit_equivalence, 1.0)
        self.assertTrue(not format.purchase_unit)
        self.assertEqual(format.purchase_unit_equivalence, 1.0)
        self.assertEqual(format.purchase_price, 0.0)
        self.assertEqual(format.is_enabled, True)
        self.assertIsInstance(format.created_at, datetime)
        self.assertIsInstance(format.enabled_at, datetime)
        self.assertEqual(format.updated_at, None)
        self.assertEqual(format.disabled_at, None)
        self.__message_publisher.execute.assert_called_once_with(
            FormatCreated(
                format.id,
                format.product_id,
                format.name,
                format.created_at,
                format.enabled_at
            )
        )

    def test_create_format_when_name_too_long_then_fail(self):
        in_memory_repository = InMemoryFormatRepository()
        needle_data_query = InMemoryCreateFormatNeedleDataQuery()
        needle_data_query.will_return(True)
        
        command = CreateFormatCommand('uuid', 'a' * 65)
        command_handler = CreateFormatCommandHandler(
            needle_data_query,
            in_memory_repository,
            self.__message_publisher
        )        
        with self.assertRaises(CreateFormatException) as context:
            command_handler.handle(command)

        self.assertEqual(context.exception.message, 'Name only accepts 64 characters')
        self.assertEqual(context.exception.key_translate, 'nameOnlyAccepts64Characters')
        self.assertIsNone(in_memory_repository.spy())
        self.__message_publisher.execute.assert_not_called()
        
    def test_create_format_when_product_does_not_exist_then_fail(self):
        in_memory_repository = InMemoryFormatRepository()
        needle_data_query = InMemoryCreateFormatNeedleDataQuery()
        needle_data_query.will_return(False)
        
        command = CreateFormatCommand('uuid', 'a' * 65)
        command_handler = CreateFormatCommandHandler(
            needle_data_query,
            in_memory_repository,
            self.__message_publisher
        )        
        with self.assertRaises(CreateFormatException) as context:
            command_handler.handle(command)

        self.assertEqual(context.exception.message, f'Product with ID {command.product_id} not found to assign format')
        self.assertEqual(context.exception.key_translate, f'productWithID{command.product_id}NotFoundToAssignFormat')
        self.assertIsNone(in_memory_repository.spy())
        self.__message_publisher.execute.assert_not_called()