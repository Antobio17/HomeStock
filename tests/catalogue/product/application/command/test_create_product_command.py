import uuid
import unittest
from datetime import datetime
from unittest.mock import Mock
from src.catalogue.product.domain.model.product import Product
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.catalogue.product.domain.event.product_created import ProductCreated
from src.catalogue.product.application.command.create_product_command import CreateProductCommand
from src.catalogue.product.domain.exception.create_product_exception import CreateProductException
from src.catalogue.product.application.command.create_product_command_handler import CreateProductCommandHandler
from src.catalogue.product.infrastructure.domain.model.in_memory.in_memory_product_repository import InMemoryProductRepository

class TestCreateProductCommand(unittest.TestCase):

    def setUp(self):
        self.__message_publisher = Mock(spec=MessagePublisher)

    def test_create_product_when_no_errors_then_success(self):
        in_memory_repository = InMemoryProductRepository()
        
        command = CreateProductCommand('Test Product')
        command_handler = CreateProductCommandHandler(
            in_memory_repository,
            self.__message_publisher
        )
        command_handler.handle(command)
        
        product = in_memory_repository.spy()

        self.assertIsInstance(product, Product)
        self.assertTrue(uuid.UUID(product.id))
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.calories, 0)
        self.assertEqual(product.carbohydrates, 0)
        self.assertEqual(product.proteins, 0)
        self.assertEqual(product.fats, 0)
        self.assertEqual(product.sugar, 0)
        self.assertEqual(product.is_enabled, True)
        self.assertIsInstance(product.created_at, datetime)
        self.assertIsInstance(product.enabled_at, datetime)
        self.assertEqual(product.updated_at, None)
        self.assertEqual(product.disabled_at, None)
        self.__message_publisher.execute.assert_called_once_with(
            ProductCreated(
                product.id,
                product.name,
                product.created_at,
                product.enabled_at
            )
        )

    def test_create_product_when_name_too_long_then_fail(self):
        in_memory_repository = InMemoryProductRepository()
        
        command = CreateProductCommand('a' * 65)
        command_handler = CreateProductCommandHandler(
            in_memory_repository,
            self.__message_publisher
        )        
        with self.assertRaises(CreateProductException) as context:
            command_handler.handle(command)

        self.assertEqual(context.exception.message, 'Name only accepts 64 characters')
        self.assertEqual(context.exception.key_translate, 'nameOnlyAccepts64Characters')
        self.assertIsNone(in_memory_repository.spy())
        self.__message_publisher.execute.assert_not_called()