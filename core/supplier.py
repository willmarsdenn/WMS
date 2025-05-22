class Supplier:
    def __init__(self, supplier_id, name, email, number):
        self.supplier_id = supplier_id
        self.name = name
        self.email = email
        self.number = number
        self.products = []

    def add_product(self, product):
        self.products.append(product)
        return f"Product {product.name} added to supplier: {self.name}."
    
    def remove_product(self, product):
        if product in self.products:
            self.products.remove(product)
            return f"Product {product.name} removed from supplier: {self.name}."
        else:
            return f"Product {product.name} not found in supplier: {self.name}."
        
    def update_email(self, new_email):
        self.email = new_email
        return f"Email updated to {self.email}"
    
    def update_number(self, new_number):
        self.number = new_number
        return f"Number updated to {self.number}"
        
    def get_supplier_info(self):
        return {
            'supplier_id': self.supplier_id,
            'name': self.name,
            'contact_info': self.contact_info,
            'products': [product.get_product_info() for product in self.products]
        }