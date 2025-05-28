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
        
    def update_quantity(self, product_id, quantity):
        if product_id in self.products:
            product, current_quantity = self.products[product_id]
            self.products[product_id] = (product, current_quantity + quantity)
        else:
            raise ValueError("Product not found in inventory.")
        
    def get_low_stock_products(self):
        return {product_id: (product, quantity, threshold) for product_id, (product, quantity, threshold) in self.products.items() if quantity < threshold}

