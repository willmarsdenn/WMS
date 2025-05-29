import pytest
from core.product import Product
from core.supplier import Supplier

class TestSupplier:
    def setup_method(self):
        self.supplier = Supplier(supplier_id=1, name="Test Supplier", email="test@supplier.co.uk", number="0709432893")
        self.product1 = Product(product_id=1, name="Product 1", description="Description 1", price=10.0, threshold=5)
        self.product2 = Product(product_id=2, name="Product 2", description="Description 2", price=20.0, threshold=3)

    def test_get_supplier_info(self):
        expected_info = {
            'supplier_id': 1,
            'name': "Test Supplier",
            'email': "test@supplier.co.uk",
            'number': "0709432893",
            'products': []
        }
        assert self.supplier.get_supplier_info() == expected_info

    def test_add_product(self):
        result = self.supplier.add_product(self.product1)
        assert result == "Product Product 1 added to supplier: Test Supplier."
        assert len(self.supplier.products) == 1
        assert self.supplier.products[0] == self.product1

    def test_remove_product(self):
        self.supplier.add_product(self.product1)
        result = self.supplier.remove_product(self.product1)
        assert result == "Product Product 1 removed from supplier: Test Supplier."
        assert len(self.supplier.products) == 0

    def test_remove_non_existent_product(self):
        result = self.supplier.remove_product(self.product1)
        assert result == "Product Product 1 not found in supplier: Test Supplier."
        assert len(self.supplier.products) == 0

    def test_update_email(self):
        new_email = "supplier@test.co.uk"
        result = self.supplier.update_email(new_email)
        assert result == f"Email updated to {new_email}"
        assert self.supplier.email == new_email

    def test_update_number(self):
        new_number = "0712345678"
        result = self.supplier.update_number(new_number)
        assert result == f"Number updated to {new_number}"
        assert self.supplier.number == new_number

    def test_add_multiple_products(self):
        self.supplier.add_product(self.product1)
        self.supplier.add_product(self.product2)
        assert len(self.supplier.products) == 2
        assert self.product1 in self.supplier.products
        assert self.product2 in self.supplier.products

    def test_get_supplier_info_with_products(self):
        self.supplier.add_product(self.product1)
        self.supplier.add_product(self.product2)
        expected_info = {
            'supplier_id': 1,
            'name': "Test Supplier",
            'email': "test@supplier.co.uk",
            'number': "0709432893",
            'products': [
                self.product1.get_product_info(),
                self.product2.get_product_info()
            ]
        }
        assert self.supplier.get_supplier_info() == expected_info