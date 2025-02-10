import uuid
import unittest
from datetime import datetime
from unittest.mock import Mock
from src.catalogue.product.domain.model.product import Product
from src.catalogue.product.domain.model.product_repository import ProductRepository
from src.catalogue.product.application.command.update_product_command import UpdateProductCommand
from src.catalogue.product.domain.exception.update_product_exception import UpdateProductException

class TestUpdateProduct(unittest.TestCase):

    def setUp(self):
        self.product_repository = Mock(spec=ProductRepository)

    def test_update_product_success(self):
        self.product_repository.find_by_id.return_value = Product(
            id = str(uuid.uuid4()),
            name = "Old Product",
            price = 5.0,
            calories = 50,
            carbohydrates = 10,
            proteins = 2,
            fats = 1,
            sugar = 5,
            is_enabled = True,
            created_at = datetime.now(),
            updated_at = datetime.now(),
            enabled_at = datetime.now(),
            disabled_at = None
        )
        
        command = UpdateProductCommand(
            id = str(uuid.uuid4()),
            name = "Test Product",
            price = 10.0,
            calories = 100,
            carbohydrates = 20,
            proteins = 5,
            fats = 2,
            sugar = 10
        )

        product = Product.update(command, self.product_repository)

        self.assertTrue(uuid.UUID(product.id))
        self.assertEqual(product.name, command.name)
        self.assertEqual(product.price, command.price)
        self.assertEqual(product.calories, command.calories)
        self.assertEqual(product.carbohydrates, command.carbohydrates)
        self.assertEqual(product.proteins, command.proteins)
        self.assertEqual(product.fats, command.fats)
        self.assertEqual(product.sugar, command.sugar)
        self.assertEqual(product.is_enabled, True)
        self.assertIsInstance(product.updated_at, datetime)
        self.assertIsInstance(product.enabled_at, datetime)
        self.assertIsNotNone(product.updated_at)

        self.product_repository.save.assert_called_once_with(product)
        
        self.assertEqual(len(product.pull_domain_events()), 1)
        


    def test_update_product_name_too_long(self):
        command = UpdateProductCommand(
            id = str(uuid.uuid4()),
            name = "a" * 65,
            price = 10.0,
            calories = 100,
            carbohydrates = 20,
            proteins = 5,
            fats = 2,
            sugar = 10
        )

        with self.assertRaises(UpdateProductException) as context:
            Product.update(command, self.product_repository)

        self.assertEqual(context.exception.message, "Name only accepts 64 characters")
        self.assertEqual(context.exception.keyTraslate, "nameOnlyAccepts64Characters")
        self.product_repository.save.assert_not_called()


    def test_update_product_negative_values(self):
        command = UpdateProductCommand(
            id = str(uuid.uuid4()),
            name = "Test Product",
            price = -1.0,
            calories = 100,
            carbohydrates = 20,
            proteins = 5,
            fats = 2,
            sugar = 10
        )

        with self.assertRaises(UpdateProductException) as context:
            Product.update(command, self.product_repository)

        self.assertEqual(context.exception.message, "All numeric fields must be greater than or equal to 0")
        self.assertEqual(context.exception.keyTraslate, "allNumericFieldsMustBeGreaterThanOrEqualToZero")
        self.product_repository.save.assert_not_called()


if __name__ == '__main__':
    unittest.main()