class Product:
    def __init__(self, product_id, name, description, price, threshold):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.threshold = threshold

    def get_product_info(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'threshold': self.threshold
        }
    
    def update_price(self, new_price):
        self.price = new_price
        return f"Price updated to {self.price}"
    
    def update_description(self, new_description):
        self.description = new_description
        return f"Description updated to {self.description}"
    
    def update_name(self, new_name):
        self.name = new_name
        return f"Name updated to {self.name}"
    
    def update_threshold(self, new_threshold):
        self.threshold = new_threshold
        return f"Threshold updated to {self.threshold}"