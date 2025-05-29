import pytest
from core.product import Product
from core.inventory import Inventory

class TestInventory:
    def setup_method(self):
        self.inventory = Inventory()
        self.product1 = Product(product_id=1, name="Product 1", description="Description 1", price=10.0, threshold=5)
        self.product2 = Product(product_id=2, name="Product 2", description="Description 2", price=20.0, threshold=3)

    def test_add_product(self):
        self.inventory.add_product(self.product1, 10)
        assert self.inventory.get_product(1) == (self.product1, 10)

    def test_remove_product(self):
        self.inventory.add_product(self.product1, 10)
        self.inventory.remove_product(1)
        assert self.inventory.get_product(1) is None

    def test_get_product(self):
        self.inventory.add_product(self.product1, 10)
        assert self.inventory.get_product(1) == (self.product1, 10)

    def test_update_quantity(self):
        self.inventory.add_product(self.product1, 10)
        self.inventory.update_quantity(1, 5)
        assert self.inventory.get_product(1) == (self.product1, 15)

    def test_get_low_stock_products(self):
        self.inventory.add_product(self.product1, 4)
        self.inventory.add_product(self.product2, 2)
        low_stock_products = self.inventory.get_low_stock_products()
        assert len(low_stock_products) == 2
        assert low_stock_products[0]['product'] == self.product1
        assert low_stock_products[0]['quantity'] == 4
        assert low_stock_products[0]['threshold'] == 5
        assert low_stock_products[1]['product'] == self.product2
        assert low_stock_products[1]['quantity'] == 2
        assert low_stock_products[1]['threshold'] == 3