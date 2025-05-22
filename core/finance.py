from datetime import datetime

class Finance:
    def __init__(self):
        self.transactions = []
        
    def record_transaction(self, order, transaction_type, amount):
        transaction = {
            'order_id': order.order_id,
            'date': datetime.now(),
            'type': transaction_type,
            'amount': amount
        }
        self.transactions.append(transaction)

    def calculate_total_sales(self):
        total_sales = sum(t['amount'] for t in self.transactions if t['type'] == 'sale')
        return total_sales
    
    def calculate_total_purchases(self):
        total_purchases = sum(t['amount'] for t in self.transactions if t['type'] == 'purchase')
        return total_purchases
    
    def calculate_profit(self):
        total_sales = self.calculate_total_sales()
        total_purchases = self.calculate_total_purchases()
        profit = total_sales - total_purchases
        return profit
    
    def generate_financial_report(self):
        total_sales = self.calculate_total_sales()
        total_purchases = self.calculate_total_purchases()
        profit = self.calculate_profit()
        
        report = {
            'total_sales': total_sales,
            'total_purchases': total_purchases,
            'profit': profit
        }
        
        return report