import pytest
from core.finance import Finance
from core.inventory import Inventory
from core.product import Product
from core.order import Order

class TestOrder:
    def setup_method(self):
        self.product1 = Product(product_id=1, name="Product 1", description="Description 1", price=10.0, threshold=5)
        self.product2 = Product(product_id=2, name="Product 2", description="Description 2", price=20.0, threshold=3)
        self.order = Order(order_id=1, order_date="2025-05-29")

    def test_add_item(self):
        result = self.order.add_item(self.product1, 5)
        assert result == "Added 5 of Product 1 to order 1."
        assert len(self.order.items) == 1
        assert self.order.items[0]['product'] == self.product1
        assert self.order.items[0]['quantity'] == 5

    def test_remove_item(self):
        self.order.add_item(self.product1, 5)
        result = self.order.remove_item(self.product1)
        assert result == "Removed Product 1 from order 1."
        assert len(self.order.items) == 0

    def test_update_status(self):
        result = self.order.update_status("Processed")
        assert result == "Order 1 status updated to Processed."
        assert self.order.status == "Processed"

    def test_get_order_summary(self):
        self.order.add_item(self.product1, 5)
        summary = self.order.get_order_summary()
        expected_summary = {
            'order_id': 1,
            'order_date': "2025-05-29",
            'supplier': None,
            'customer': None,
            'items': [('Product 1', 5)],
            'status': "Created - Not Processed"
        }
        assert summary == expected_summary

    def test_process_order_purchase(self):
        inventory = Inventory()
        finance = Finance()
        self.order.supplier = type('Supplier', (object,), {'name': 'Supplier 1'})

        inventory.add_product(self.product1, 10)
        inventory.add_product(self.product2, 5)

        self.order.add_item(self.product1, 5)
        self.order.add_item(self.product2, 3)

        result = self.order.process_order(inventory, finance)
        assert result == "Order 1 processed successfully."
        assert inventory.get_product(1) == (self.product1, 15)
        assert inventory.get_product(2) == (self.product2, 8)
        assert finance.calculate_total_purchases() == 110.0

    def test_process_order_sale(self):
        inventory = Inventory()
        finance = Finance()
        self.order.customer = type('Customer', (object,), {'name': 'Customer 1'})
        self.order.add_item(self.product1, 2)
        self.order.add_item(self.product2, 1)

        inventory.add_product(self.product1, 10)
        inventory.add_product(self.product2, 5)

        result = self.order.process_order(inventory, finance)
        assert result == "Order 1 processed successfully."
        assert inventory.get_product(1) == (self.product1, 8)
        assert inventory.get_product(2) == (self.product2, 4)
        assert finance.calculate_total_sales() == 40.0