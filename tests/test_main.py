import pytest
from core.product import Product
from core.supplier import Supplier
from core.inventory import Inventory
from core.order import Order
from core.finance import Finance
from datetime import datetime

class TestIntegration:
    def setup_method(self):
        self.inventory = Inventory()
        self.finance = Finance()
        
        self.particle_accelerator = Product(1, "Particle Accelerator", "Particle Accelerator", 1299.99, 5)
        self.super_computer = Product(2, "Super Computer", "Super Computer", 29.99, 10)
        self.quantum_computer = Product(3, "Quantum Computer", "Quantum Computer", 89.99, 8)
        
        self.inventory.add_product(self.particle_accelerator, 10)
        self.inventory.add_product(self.super_computer, 20) 
        self.inventory.add_product(self.quantum_computer, 5)
        
        self.supplier = Supplier(1, "Science and Technology Facilities Council", "test@stfc.ac.uk", "07483278492")
        self.supplier.add_product(self.particle_accelerator)
        self.supplier.add_product(self.super_computer)
        self.supplier.add_product(self.quantum_computer)
        
        self.customer = {"name": "Will Marsden"}
        
    def test_full_purchase_flow(self):
        purchase_order = Order(1, datetime.now(), supplier=self.supplier)
        purchase_order.add_item(self.quantum_computer, 15)
        
        result = purchase_order.process_order(self.inventory, self.finance)
        assert "processed successfully" in result
        
        quantum_computer_data = self.inventory.get_product(3)
        assert quantum_computer_data is not None
        assert quantum_computer_data[1] == 20
        
        assert len(self.finance.transactions) == 1
        assert self.finance.transactions[0]['type'] == "purchase"
        assert self.finance.transactions[0]['amount'] == 15 * self.quantum_computer.price
        
    def test_full_sales_flow(self):
        sales_order = Order(1, datetime.now(), customer=self.customer)
        sales_order.add_item(self.particle_accelerator, 2)
        sales_order.add_item(self.super_computer, 5)
        
        result = sales_order.process_order(self.inventory, self.finance)
        assert "processed successfully" in result
        
        particle_accelerator_data = self.inventory.get_product(1)
        super_computer_data = self.inventory.get_product(2)
        assert particle_accelerator_data[1] == 8
        assert super_computer_data[1] == 15
        
        assert len(self.finance.transactions) == 1
        assert self.finance.transactions[0]['type'] == "sale"
        expected_amount = (2 * self.particle_accelerator.price) + (5 * self.super_computer.price)
        assert self.finance.transactions[0]['amount'] == expected_amount
        
    def test_low_stock_reporting(self):
        self.inventory.update_quantity(1, -6)
        self.inventory.update_quantity(2, 150)
        self.inventory.update_quantity(3, 150)

        low_stock = self.inventory.get_low_stock_products()

        assert len(low_stock) == 1
        assert low_stock[0]['quantity'] == 4
        assert low_stock[0]['threshold'] == 5

        self.inventory.update_quantity(2, -150)
        self.inventory.update_quantity(3, -150)
        
    def test_financial_reporting(self):
        purchase_order = Order(1, datetime.now(), supplier=self.supplier)
        purchase_order.add_item(self.quantum_computer, 10)
        purchase_order.process_order(self.inventory, self.finance)
        
        sales_order = Order(1, datetime.now(), customer=self.customer)
        sales_order.add_item(self.particle_accelerator, 2)
        sales_order.process_order(self.inventory, self.finance)
        
        report = self.finance.generate_financial_report()
        
        expected_purchases = 10 * self.quantum_computer.price
        expected_sales = 2 * self.particle_accelerator.price
        expected_profit = expected_sales - expected_purchases
        
        assert report['total_purchases'] == expected_purchases
        assert report['total_sales'] == expected_sales
        assert report['profit'] == expected_profit