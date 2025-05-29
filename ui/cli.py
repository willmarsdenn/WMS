import cmd
import random
from datetime import datetime
from core.product import Product
from core.supplier import Supplier
from core.order import Order

class CLI(cmd.Cmd):
    startmsg = "Welcome to WMS! Type help to list commands.\n"
    prompt = "User> "

    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.intro = self.startmsg
        self.prompt = self.prompt
    
    def _validate_args(self, args, expected_count, usage):
        if len(args) != expected_count:
            print(f"Error: Incorrect number of arguments")
            print(f"Usage: {usage}")
            return False
        return True
    
    def _get_supplier(self, supplier_id):
        for s in self.ui.suppliers:
            if s.supplier_id == supplier_id:
                return s
        print(f"Supplier {supplier_id} not found")
        return None
    
    def _get_product(self, product_id):
        product_data = self.ui.inventory.get_product(product_id)
        if not product_data:
            print(f"Product {product_id} not found in inventory")
            return None
        return product_data
    
    def _require_current_order(self):
        if not self.ui.current_order:
            print("Error: No active order. Create a purchase or sales order first.")
            return False
        return True
    
    def _display_inventory(self, title="Current Inventory:"):
        if not self.ui.inventory.products:
            print("No products in inventory")
            return
            
        print(f"\n{title}")
        print("-" * 80)
        print(f"{'ID':<10}{'Name':<25}{'Price':<10}{'Quantity':<10}{'Threshold':<10}")
        print("-" * 80)
        
        for product_id, (product, quantity) in self.ui.inventory.products.items():
            print(f"{product_id:<10}{product.name:<25}£{product.price:<9.2f}{quantity:<10}{product.threshold:<10}")
    
    def _handle_error(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def do_add_product(self, arg):
        try:
            args = arg.split(None, 5)
            if not self._validate_args(args, 6, "add_product product_id name description price threshold quantity"):
                return
            
            product_id, name, description, price, threshold, quantity = args
            try:
                price = float(price)
                threshold = int(threshold)
                quantity = int(quantity)
            except ValueError:
                print("Error: Price must be a number, threshold and quantity must be integers")
                return
                
            product = Product(product_id, name, description, price, threshold)
            self.ui.inventory.add_product(product, quantity)
            print(f"Added {quantity} units of {name} to inventory")
        except Exception as e:
            print(f"Error: {e}")
    
    def do_list_inventory(self, arg):
        self._display_inventory()
    
    def do_add_supplier(self, arg):
        try:
            args = arg.split(None, 3)
            if not self._validate_args(args, 4, "add_supplier supplier_id name email phone_number"):
                return
                
            supplier_id, name, email, number = args
            supplier = Supplier(supplier_id, name, email, number)
            self.ui.suppliers.append(supplier)
            print(f"Added supplier: {name}")
        except Exception as e:
            print(f"Error: {e}")
    
    def do_list_suppliers(self, arg):
        if not self.ui.suppliers:
            print("No suppliers in the system")
            return
            
        print("\nSuppliers:")
        print("-" * 80)
        print(f"{'ID':<10}{'Name':<25}{'Email':<30}{'Phone':<15}")
        print("-" * 80)
        
        for supplier in self.ui.suppliers:
            print(f"{supplier.supplier_id:<10}{supplier.name:<25}{supplier.email:<30}{supplier.number:<15}")
    
    def do_supplier_add_product(self, arg):
        try:
            args = arg.split()
            if not self._validate_args(args, 2, "supplier_add_product supplier_id product_id"):
                return
                
            supplier_id, product_id = args
            
            supplier = self._get_supplier(supplier_id)
            if not supplier:
                return
                
            product_data = self._get_product(product_id)
            if not product_data:
                return
                
            product, _ = product_data
            result = supplier.add_product(product)
            print(result)
            
        except Exception as e:
            print(f"Error: {e}")
    
    def do_create_purchase_order(self, arg):
        try:
            args = arg.split()
            if not self._validate_args(args, 2, "create_purchase_order order_id supplier_id"):
                return
                
            order_id, supplier_id = args
            
            supplier = self._get_supplier(supplier_id)
            if not supplier:
                return
                
            self.ui.current_order = Order(order_id, datetime.now(), supplier=supplier)
            print(f"Created purchase order {order_id} with supplier {supplier.name}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    def do_create_sales_order(self, arg):
        try:
            parts = arg.split(None, 1)
            if not self._validate_args(parts, 2, "create_sales_order order_id customer_name"):
                return
                
            order_id, customer_name = parts
            
            customer = {"name": customer_name}
            self.ui.current_order = Order(order_id, datetime.now(), customer=customer)
            print(f"Created sales order {order_id} for customer {customer_name}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    def do_add_order_item(self, arg):
        if not self._require_current_order():
            return
            
        try:
            args = arg.split()
            if not self._validate_args(args, 2, "add_order_item product_id quantity"):
                return
                
            product_id, quantity = args
            try:
                quantity = int(quantity)
            except ValueError:
                print("Error: Quantity must be an integer")
                return
                
            product_data = self._get_product(product_id)
            if not product_data:
                return
                
            product, curr_quantity = product_data
            
            if self.ui.current_order.customer and quantity > curr_quantity:
                print(f"Error: Not enough inventory. Requested: {quantity}, Available: {curr_quantity}")
                return
                
            result = self.ui.current_order.add_item(product, quantity)
            print(result)
            
        except Exception as e:
            print(f"Error: {e}")
    
    def do_remove_order_item(self, arg):
        if not self._require_current_order():
            return
            
        try:
            product_id = arg.strip()
            if not product_id:
                print("Error: Please provide a product ID")
                return
                
            product_data = self._get_product(product_id)
            if not product_data:
                return
                
            product, _ = product_data
            result = self.ui.current_order.remove_item(product)
            print(result)
            
        except Exception as e:
            print(f"Error: {e}")
    
    def do_show_order(self, arg):
        if not self._require_current_order():
            return
            
        order = self.ui.current_order
        summary = order.get_order_summary()
        
        print("\nOrder Details:")
        print("-" * 80)
        print(f"Order ID: {summary['order_id']}")
        print(f"Date: {summary['order_date']}")
        
        if summary['supplier']:
            print(f"Supplier: {summary['supplier']}")
        elif summary['customer']:
            print(f"Customer: {summary['customer']}")
            
        print(f"Status: {summary['status']}")
        print("\nItems:")
        print("-" * 80)
        print(f"{'Product':<30}{'Quantity':<10}")
        print("-" * 80)
        
        for product_name, quantity in summary['items']:
            print(f"{product_name:<30}{quantity:<10}")
    
    def do_process_order(self, arg):
        if not self._require_current_order():
            return
            
        result = self.ui.current_order.process_order(self.ui.inventory, self.ui.finance)
        print(result)
        
        self._display_inventory("Updated Inventory:")
        
        self.ui.current_order = None
    
    def do_financial_report(self, arg):
        report = self.ui.finance.generate_financial_report()
        
        print("\nFinancial Report:")
        print("-" * 50)
        print(f"Total Sales: £{report['total_sales']:.2f}")
        print(f"Total Purchases: £{report['total_purchases']:.2f}")
        print(f"Profit: £{report['profit']:.2f}")
    
    def do_low_stock_report(self, arg):
        low_stock = self.ui.inventory.get_low_stock_products()
        
        if not low_stock:
            print("No products are below their threshold")
            return
            
        print("\nLow Stock Report:")
        print("-" * 80)
        print(f"{'ID':<10}{'Name':<25}{'Current Stock':<15}{'Threshold':<10}{'Need to Order':<15}")
        print("-" * 80)
        
        for item in low_stock:
            product = item['product']
            quantity = item['quantity']
            threshold = item['threshold']
            need_to_order = threshold - quantity
            
            print(f"{product.product_id:<10}{product.name:<25}{quantity:<15}{threshold:<10}{need_to_order:<15}")
    
    def do_exit(self, arg):
        print("Thank you for using WMS. Goodbye!")
        return True
        
    def do_quit(self, arg):
        return self.do_exit(arg)
    
    def do_help(self, arg):
        cmd.Cmd.do_help(self, arg)
        
    def emptyline(self):
        pass