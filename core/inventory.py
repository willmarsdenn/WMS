class Inventory:
    def __init__(self):
        self.products = {}
        
    def add_product(self, product, quantity):
        if product.product_id in self.products:
            self.update_quantity(product.product_id, quantity)
        else:
            self.products[product.product_id] = (product, quantity)

    def remove_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
        else:
            raise ValueError("Product not found in inventory.")
        
    def get_product(self, product_id):
        if product_id in self.products:
            return self.products[product_id]
        return None
        
    def update_quantity(self, product_id, quantity):
        if product_id in self.products:
            product, current_quantity = self.products[product_id]
            self.products[product_id] = (product, current_quantity + quantity)
        else:
            raise ValueError("Product not found in inventory.")
        
    def get_low_stock_products(self):
        low_stock = []
        for product_id, quantity in self.products.items():
            product = self.get_product(product_id)

            if product and quantity < product.threshold:
                low_stock.append({
                    'product': product,
                    'quantity': quantity,
                    'threshold': product.threshold
                })
            
        return low_stock
