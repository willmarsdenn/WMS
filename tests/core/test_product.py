import pytest
from core.product import Product

class TestProduct:
    def setup_method(self):
        self.product = Product(product_id=1, name="Test Product", description="A test product", price=100.0, threshold=10)

    def test_get_product_info(self):
        expected_info = {
            'product_id': 1,
            'name': "Test Product",
            'description': "A test product",
            'price': 100.0,
            'threshold': 10
        }
        assert self.product.get_product_info() == expected_info

    def test_update_price(self):
        new_price = 120.0
        assert self.product.update_price(new_price) == f"Price updated to {new_price}"
        assert self.product.price == new_price

    def test_update_description(self):
        new_description = "Updated description"
        assert self.product.update_description(new_description) == f"Description updated to {new_description}"
        assert self.product.description == new_description

    def test_update_name(self):
        new_name = "Updated Product Name"
        assert self.product.update_name(new_name) == f"Name updated to {new_name}"
        assert self.product.name == new_name

    def test_update_threshold(self):
        new_threshold = 5
        assert self.product.update_threshold(new_threshold) == f"Threshold updated to {new_threshold}"
        assert self.product.threshold == new_threshold