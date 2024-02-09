# Inside reset_product_ratings.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DarazMall.settings')
django.setup()

from main.models import Product

def reset_product_ratings():
    products = Product.objects.all()
    for product in products:
        product.rating = 0
        product.save()
    print('Product ratings reset successfully')

if __name__ == "__main__":
    reset_product_ratings()
