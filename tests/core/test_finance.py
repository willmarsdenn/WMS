import pytest
from core.finance import Finance

class TestFinance:
    def setup_method(self):
        self.finance = Finance()

    def test_record_transaction(self):
        order = type('Order', (object,), {'order_id': 1})()
        transaction_type = 'sale'
        amount = 100.0
        self.finance.record_transaction(order, transaction_type, amount)
        assert len(self.finance.transactions) == 1
        assert self.finance.transactions[0]['order_id'] == order.order_id
        assert self.finance.transactions[0]['type'] == transaction_type
        assert self.finance.transactions[0]['amount'] == amount

    def test_calculate_total_sales(self):
        order1 = type('Order', (object,), {'order_id': 1})()
        order2 = type('Order', (object,), {'order_id': 2})()
        self.finance.record_transaction(order1, 'sale', 100.0)
        self.finance.record_transaction(order2, 'sale', 200.0)
        assert self.finance.calculate_total_sales() == 300.0

    def test_calculate_total_purchases(self):
        order1 = type('Order', (object,), {'order_id': 1})()
        order2 = type('Order', (object,), {'order_id': 2})()
        self.finance.record_transaction(order1, 'purchase', 150.0)
        self.finance.record_transaction(order2, 'purchase', 250.0)
        assert self.finance.calculate_total_purchases() == 400.0

    def test_calculate_profit(self):
        order1 = type('Order', (object,), {'order_id': 1})()
        order2 = type('Order', (object,), {'order_id': 2})()
        self.finance.record_transaction(order1, 'sale', 500.0)
        self.finance.record_transaction(order2, 'purchase', 300.0)
        assert self.finance.calculate_profit() == 200.0

    def test_generate_financial_report(self):
        order1 = type('Order', (object,), {'order_id': 1})()
        order2 = type('Order', (object,), {'order_id': 2})()
        self.finance.record_transaction(order1, 'sale', 500.0)
        self.finance.record_transaction(order2, 'purchase', 300.0)
        
        report = self.finance.generate_financial_report()
        assert report['total_sales'] == 500.0
        assert report['total_purchases'] == 300.0
        assert report['profit'] == 200.0