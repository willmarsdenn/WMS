from core.inventory import Inventory
from core.supplier import Supplier
from core.finance import Finance

class Order:
    def __init__(self, order_id, order_date, supplier=None, customer=None):
        self.order_id = order_id
        self.order_date = order_date
        self.supplier = supplier
        self.customer = customer
        self.items = []
        self.status = "Created - Not Processed"

    def add_item(self, product, quantity):
        self.items.append({'product': product, 'quantity': quantity})
        return f"Added {quantity} of {product.name} to order {self.order_id}."
    
    def remove_item(self, product):
        for item in self.items:
            if item['product'] == product:
                self.items.remove(item)
                return f"Removed {product.name} from order {self.order_id}."
        return f"Product {product.name} not found in order {self.order_id}."
    
    def update_status(self, new_status):
        self.status = new_status
        return f"Order {self.order_id} status updated to {self.status}."
    
    def get_order_summary(self):
        summary = {
            'order_id': self.order_id,
            'order_date': self.order_date,
            'supplier': self.supplier.name if self.supplier else None,
            'customer': self.customer.name if self.customer else None,
            'items': [(item['product'].name, item['quantity']) for item in self.items],
            'status': self.status
        }
        return summary
    
    def process_order(self, inventory, finance=None):

        self.update_status("Processing")

        is_purchase = self.supplier is not None
        is_sale = self.customer is not None

        if not self.items:
            return "Can't process empty order"

        total_amount = 0

        for item in self.items:
            product = item['product']
            quantity = item['quantity']

            if is_purchase:
                inventory.update_quantity(product.product_id, quantity)
                total_amount += product.price * quantity

            elif is_sale:
                inventory.update_quantity(product.product_id, -quantity)
                total_amount += product.price * quantity

        if finance and total_amount > 0:
            transaction_type = "purchase" if is_purchase else "sale"
            finance.record_transaction(self, transaction_type, total_amount)

        self.update_status("Completed - Processed")

        return f"Order {self.order_id} processed successfully."