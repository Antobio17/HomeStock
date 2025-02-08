import uuid
import unittest
from datetime import datetime
from unittest.mock import Mock
from src.catalogue.product.domain.model.product import Product
from src.catalogue.product.domain.model.product_repository import ProductRepository
from src.catalogue.product.application.command.create_product_command import CreateProductCommand
from src.catalogue.product.domain.exception.create_product_exception import CreateProductException

class TestCreateProduct(unittest.TestCase):

    def setUp(self):
        self.product_repository = Mock(spec=ProductRepository)

    def test_create_product_success(self):
        command = CreateProductCommand(
            name="Test Product",
            price=10.0,
            calories=100,
            carbohydrates=20,
            proteins=5,
            fats=2,
            sugar=10,
            is_enabled=True
        )

        product = Product.create(command, self.product_repository)

        self.assertIsInstance(product, Product)
        self.assertTrue(uuid.UUID(product.id))
        self.assertEqual(product.name, command.name)
        self.assertEqual(product.price, command.price)
        self.assertEqual(product.calories, command.calories)
        self.assertEqual(product.carbohydrates, command.carbohydrates)
        self.assertEqual(product.proteins, command.proteins)
        self.assertEqual(product.fats, command.fats)
        self.assertEqual(product.sugar, command.sugar)
        self.assertEqual(product.is_enabled, command.is_enabled)
        self.assertIsInstance(product.created_at, datetime)
        self.assertIsInstance(product.enabled_at, datetime)
        self.assertEqual(product.updated_at, None)
        self.assertEqual(product.disabled_at, None)

        self.product_repository.save.assert_called_once_with(product)
        
        self.assertEqual(len(product.pull_domain_events()), 1)
        


    def test_create_product_name_too_long(self):
        command = CreateProductCommand(
            name="a" * 65,
            price=10.0,
            calories=100,
            carbohydrates=20,
            proteins=5,
            fats=2,
            sugar=10,
            is_enabled=True
        )

        with self.assertRaises(CreateProductException) as context:
            Product.create(command, self.product_repository)

        self.assertEqual(context.exception.message, "Name only accepts 64 characters")
        self.assertEqual(context.exception.keyTraslate, "nameOnlyAccepts64Characters")
        self.product_repository.save.assert_not_called()


    def test_create_product_negative_values(self):
        command = CreateProductCommand(
            name="Test Product",
            price=-1.0,
            calories=100,
            carbohydrates=20,
            proteins=5,
            fats=2,
            sugar=10,
            is_enabled=True
        )

        with self.assertRaises(CreateProductException) as context:
            Product.create(command, self.product_repository)

        self.assertEqual(context.exception.message, "All numeric fields must be greater than or equal to 0")
        self.assertEqual(context.exception.keyTraslate, "allNumericFieldsMustBeGreaterThanOrEqualToZero")
        self.product_repository.save.assert_not_called()


if __name__ == '__main__':
    unittest.main()