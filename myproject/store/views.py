from django.shortcuts import render
from .models import Product
import random

def product_list(request):
    products = Product.objects.all()  # Query all products from the database
    return render(request, 'store/product_list.html', {'products': products})

def home(request):
    # Fetch all products and select a random subset
    products = list(Product.objects.all())
    random_products = random.sample(products, min(len(products), 5))  # Show up to 5 random products
    return render(request, 'store/home.html', {'random_products': random_products})