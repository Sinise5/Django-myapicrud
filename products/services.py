# 10. Implementasi Service Layer untuk Product di products/services.py
from .models import Product

class ProductService:
    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    @staticmethod
    def get_product_by_id(product_id):
        return Product.objects.filter(id=product_id).first()
    
    @staticmethod
    def create_product(name, description, price):
        return Product.objects.create(name=name, description=description, price=price)
    
    @staticmethod
    def update_product(product, data):
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product
    
    @staticmethod
    def delete_product(product):
        product.delete()